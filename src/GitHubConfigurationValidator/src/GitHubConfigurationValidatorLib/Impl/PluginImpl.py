# ----------------------------------------------------------------------
# |
# |  PluginImpl.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 10:41:38
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains functions that make it easy to generate Plugin objects"""

import textwrap

from dataclasses import dataclass
from typing import Any, Callable, Generic, Optional, Type as PythonType, TypeVar

import typer

from semantic_version import Version as SemVer

from Common_Foundation.Types import overridemethod
from Common_FoundationEx.TyperEx import TypeDefinitionsType

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase


# ----------------------------------------------------------------------
# |
# |  Public Types
# |
# ----------------------------------------------------------------------
ResultT                                     = TypeVar("ResultT")

@dataclass(frozen=True)
class Result(Generic[ResultT]):
    """Object used to distinguish between  a PluginBase.ValidateResultType and an actual result"""
    result: ResultT


# ----------------------------------------------------------------------
# |
# |  Public Functions
# |
# ----------------------------------------------------------------------
def CreateEnablePlugin(
    name: str,
    configuration_type: PluginBase.ConfigurationType,
    version_introduced: SemVer,
    instantiation_parameter_default_value: bool,
    instantiation_parameter_flag_name: str,
    github_settings_url_suffix: str,
    github_settings_section: str,
    github_settings_value: Optional[str],
    get_configuration_value_func: Callable[[dict[str, Any]], PluginBase.ValidateResultType | bool],
    subject: Optional[str]=None,
) -> PythonType:
    """Creates a Plugin class for plugins that check if a value is enabled or disabled."""

    if github_settings_value is None:
        github_settings_value = "the value"
    else:
        github_settings_value = "'{}'".format(github_settings_value)

    if not subject:
        subject = github_settings_value

    instantiation_parameter_name = _CreateParameterName()

    # ----------------------------------------------------------------------
    # pylint: disable=missing-class-docstring
    class Plugin(PluginBase):
        # ----------------------------------------------------------------------
        @classmethod
        @overridemethod
        def GetInstantiationParameters(cls) -> TypeDefinitionsType:

            return {
                instantiation_parameter_name: (
                    bool,
                    typer.Option(
                        instantiation_parameter_default_value,
                        instantiation_parameter_flag_name,
                        help="Indicates that {} should be {}.".format(
                            subject,
                            "enabled" if instantiation_parameter_default_value else "disabled",
                        ),
                    ),
                ),
            }

        # ----------------------------------------------------------------------
        def __init__(
            self,
            **kwargs,
        ):
            enable_value = kwargs[instantiation_parameter_name]
            enable_desc = "enabled" if enable_value else "disabled"

            super(Plugin, self).__init__(
                name,
                configuration_type,
                version_introduced,
                "Validates that {} is {}.".format(subject, enable_desc),
                textwrap.dedent(
                    """\
                    1) Visit '{{repository}}/{github_settings_url_suffix}'
                    2) Locate the '{github_settings_section}' section
                    3) Ensure that {github_settings_value} is {checked_desc}
                    """,
                ).format(
                    github_settings_url_suffix=github_settings_url_suffix,
                    github_settings_section=github_settings_section,
                    github_settings_value=github_settings_value,
                    checked_desc="checked" if enable_value else "unchecked",
                ),
            )

            self._enable_value              = enable_value
            self._enable_desc               = enable_desc

        # ----------------------------------------------------------------------
        @overridemethod
        def Validate(
            self,
            configuration: dict[str, Any],
        ) -> PluginBase.ValidateResultType:
            result = get_configuration_value_func(configuration)
            if result is not None:
                if not isinstance(result, bool):
                    return result

                if result != self._enable_value:
                    return "{} is not {}.\n".format(subject, self._enable_desc)

            return None

    # ----------------------------------------------------------------------

    return Plugin


# ----------------------------------------------------------------------
CreateValuePluginT                          = TypeVar("CreateValuePluginT")

def CreateValuePlugin(
    name: str,
    configuration_type: PluginBase.ConfigurationType,
    version_introduced: SemVer,
    instantiation_parameter_default_value: CreateValuePluginT,
    instantiation_parameter_flag_name: str,
    github_settings_url_suffix: str,
    github_settings_section: Optional[str],
    github_settings_value: Optional[str],
    get_configuration_value_func: Callable[[dict[str, Any]], PluginBase.ValidateResultType | Result[Optional[CreateValuePluginT]]],
    subject: Optional[str]=None,
) -> PythonType:
    if github_settings_value is None:
        github_settings_value = "the value"
    else:
        github_settings_value = "'{}'".format(github_settings_value)

    if not subject:
        subject = github_settings_value

    instantiation_parameter_name = _CreateParameterName()

    # ----------------------------------------------------------------------
    # pylint: disable=missing-class-docstring
    class Plugin(PluginBase):
        # ----------------------------------------------------------------------
        @classmethod
        @overridemethod
        def GetInstantiationParameters(cls) -> TypeDefinitionsType:
            return {
                instantiation_parameter_name: (
                    str,
                    typer.Option(
                        instantiation_parameter_default_value,
                        instantiation_parameter_flag_name,
                        help="Value for {} provided to the '{}' plugin.".format(subject, name),
                    ),
                ),
            }

        # ----------------------------------------------------------------------
        def __init__(
            self,
            **kwargs,
        ):
            value = kwargs[instantiation_parameter_name]

            if isinstance(value, str) and value.lower() in ["null", "none"]:
                value = None

            if value is not None and isinstance(instantiation_parameter_default_value, int):
                value = int(value)

            if github_settings_section is None:
                resolution_instructions = "No Resolution Instructions are available."
            else:
                resolution_instructions = textwrap.dedent(
                    """\
                    1) Visit '{{repository}}/{github_settings_url_suffix}'
                    2) Locate the '{github_settings_section}' section
                    3) Ensure that {github_settings_value} is set to '{set_value}'.
                    """,
                ).format(
                    github_settings_url_suffix=github_settings_url_suffix,
                    github_settings_section=github_settings_section,
                    github_settings_value=github_settings_value,
                    set_value=value,
                )

            super(Plugin, self).__init__(
                name,
                configuration_type,
                version_introduced,
                "Validates that {} is set to '{}'.".format(subject, value),
                resolution_instructions,
            )

            self._expected_value            = value

        # ----------------------------------------------------------------------
        @overridemethod
        def Validate(
            self,
            configuration: dict[str, Any],
        ) -> PluginBase.ValidateResultType:
            result = get_configuration_value_func(configuration)
            if result is not None:
                if not isinstance(result, Result):
                    return result

                if result.result != self._expected_value:
                    return "{} is not set to '{}' (currently set to '{}').\n".format(
                        subject,
                        self._expected_value,
                        result.result,
                    )

            return None

    # ----------------------------------------------------------------------

    return Plugin


# ----------------------------------------------------------------------
# |
# |  Private Data
# |
# ----------------------------------------------------------------------
_parameter_ctr: int                         = 0


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
def _CreateParameterName() -> str:
    global _parameter_ctr  # pylint: disable=global-statement

    result = "parameter{}".format(_parameter_ctr)
    _parameter_ctr += 1

    return result
