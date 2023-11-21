# ----------------------------------------------------------------------
# |
# |  Plugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 09:17:42
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the Plugin object"""

import re
import textwrap

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Type as PythonType, Union

from semantic_version import Version as SemVer

from Common_Foundation.Streams.DoneManager import DoneManager
from Common_Foundation import TextwrapEx
from Common_Foundation.Types import extensionmethod

from Common_FoundationEx.TyperEx import typer, TypeDefinitionItem, TypeDefinitionsType

from GitHubConfigurationValidatorLib.GitHubSession import GitHubSession


# ----------------------------------------------------------------------
class Plugin(ABC):
    """Plugin that validates GitHub settings"""

    # ----------------------------------------------------------------------
    # |
    # |  Public Types
    # |
    # ----------------------------------------------------------------------
    class ConfigurationType(Enum):
        """Categories to differentiate between the different GitHub configuration types"""

        Repository                          = auto()
        Branch                              = auto()
        BranchProtection                    = auto()
        Custom                              = auto()

    # ----------------------------------------------------------------------
    class MessageType(Enum):
        """Categories to differentiate between message types"""
        Warning                             = auto()
        Error                               = auto()
        Info                                = auto()

    # ----------------------------------------------------------------------
    ValidateResultItemType                  = Union[
        str,                                # Error message
        tuple["Plugin.MessageType", str],
    ]

    # ----------------------------------------------------------------------
    ValidateResultType                      = Union[
        None,                                           # No errors, warnings, or info messages
        "Plugin.ValidateResultItemType",                # Single error, warning, or info message
        list["Plugin.ValidateResultItemType"],          # Multiple errors/warnings/info messages
    ]

    # ----------------------------------------------------------------------
    # |
    # |  Public Methods
    # |
    # ----------------------------------------------------------------------
    @classmethod
    def GetInstantiationParameters(cls) -> TypeDefinitionsType:
        """\
        Returns parameters that can be provided on the command line and used to alter the behavior of the plugin.
        Once resolved from the command line, these parameters are passed to the derived Plugin during
        instantiation.
        """

        # By default, no arguments are provided
        return {}

    # ----------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        configuration_type: "Plugin.ConfigurationType",
        version_introduced: SemVer,
        description: str,
        resolution_description: str,
        rationale: Optional[str]=None,
    ):
        if not self.__class__._NAME_VALIDATION_EXPR.match(name):
            raise Exception("'{}' is not a valid plugin name.".format(name))

        self.name                           = name
        self.configuration_type             = configuration_type
        self.version_introduced             = version_introduced
        self.description                    = description
        self.resolution_description         = resolution_description
        self.rationale                      = rationale

    # ----------------------------------------------------------------------
    @abstractmethod
    def Validate(
        self,
        configuration: dict[str, Any],
    ) -> "Plugin.ValidateResultType":
        """Validates the provided configuration, returning messages that should be displayed to the caller"""

        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    @extensionmethod
    def CustomValidate(
        self,
        dm: DoneManager,
        session: GitHubSession,
        repository: str,
    ) -> "Plugin.ValidateResultType":
        """Perform complex validation via a session object."""

        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    def GenerateDisplayString(
        self,
        *,
        include_header: bool=True,
        include_parameters: bool=True,
        resolution_repository: Optional[str]=None,  # resolution information will be provided if this value is not None
        include_rationale: bool=True,
    ) -> str:
        components: list[str] = []

        # Write the header last, as it will impact everything else that is written.

        if include_parameters:
            # ----------------------------------------------------------------------
            @dataclass
            class TyperInfo(object):
                command_line_arg: str
                description: str

            # ----------------------------------------------------------------------
            def GetTyperInfo(
                typer_info: typer.models.OptionInfo,
            ) -> TyperInfo:
                return TyperInfo(
                    typer_info.param_decls[0],
                    typer_info.help,
                )

            # ----------------------------------------------------------------------

            parameters = self.__class__.GetInstantiationParameters()
            if parameters:
                items: dict[str, str] = {}

                for type_definition_type in parameters.values():
                    python_type: Optional[PythonType] = None
                    typer_info: Optional[TyperInfo] = None

                    if isinstance(type_definition_type, TypeDefinitionItem):
                        python_type = type_definition_type.python_type
                        typer_info = GetTyperInfo(type_definition_type.option_info)

                    elif (
                        isinstance(type_definition_type, tuple)
                        and len(type_definition_type) == 2
                        and isinstance(type_definition_type[0], PythonType)
                        and isinstance(type_definition_type[1], typer.models.OptionInfo)
                    ):
                        python_type = type_definition_type[0]
                        typer_info = GetTyperInfo(type_definition_type[1])

                    else:
                        assert False, type_definition_type

                    assert python_type is not None
                    assert typer_info is not None

                    if python_type is bool:
                        items[typer_info.command_line_arg] = typer_info.description
                    else:
                        items["{} <{}>".format(
                            typer_info.command_line_arg,
                            python_type.__name__,
                        )] = typer_info.description

                max_item_length = max(len(k) for k in items.keys())
                item_template = "{{:<{}}}: {{}}".format(int(max_item_length * 1.2))

                components.append(
                    textwrap.dedent(
                        """\
                        -------------------------
                        Command Line Parameter(s)
                        -------------------------
                        {}

                        """,
                    ).format(
                        "\n".join(item_template.format(k, v) for k, v in items.items())
                    ),
                )

        if resolution_repository:
            components.append(
                textwrap.dedent(
                    """\
                    ----------
                    Resolution
                    ----------
                    {}

                    """,
                ).format(
                    self.resolution_description.format(
                        repository=resolution_repository,
                    ).rstrip(),
                ),
            )

        if include_rationale and self.rationale:
            components.append(
                textwrap.dedent(
                    """\
                    ---------
                    Rationale
                    ---------
                    {}

                    """,
                ).format(
                    self.rationale.rstrip(),
                ),
            )

        components_str = "".join(components)

        if not include_header:
            return components_str

        return textwrap.dedent(
            """\
            {name_underline}
              {name}
            {name_underline}

                Configuration Type:  {configuration_type}
                Version Introduced:  {version_introduced}

                -----------
                Description
                -----------
                {description}

                {components}

            """,
        ).format(
            name=self.name,
            name_underline="=" * (len(self.name) + 4),
            configuration_type=self.configuration_type.name,
            version_introduced=self.version_introduced,
            description=TextwrapEx.Indent(
                self.description.rstrip(),
                4,
                skip_first_line=True,
            ),
            components=TextwrapEx.Indent(
                components_str.rstrip(),
                4,
                skip_first_line=True,
            ),
        )

    # ----------------------------------------------------------------------
    # |
    # |  Private Data
    # |
    # ----------------------------------------------------------------------
    _NAME_VALIDATION_EXPR                   = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")
