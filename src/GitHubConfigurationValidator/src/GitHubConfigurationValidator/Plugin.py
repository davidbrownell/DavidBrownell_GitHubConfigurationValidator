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

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Union

from Common_Foundation.Types import extensionmethod

from Common_FoundationEx.TyperEx import TypeDefinitionsType


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
        description: str,
        resolution_description: str,
    ):
        if not self.__class__._NAME_VALIDATION_EXPR.match(name):
            raise Exception("'{}' is not a valid plugin name.".format(name))

        self.name                           = name
        self.configuration_type             = configuration_type
        self.description                    = description
        self.resolution_description         = resolution_description

    # ----------------------------------------------------------------------
    @abstractmethod
    def Validate(
        self,
        configuration: dict[str, Any],
    ) -> "Plugin.ValidateResultType":
        """Validates the provided configuration, returning messages that should be displayed to the caller"""

        raise Exception("Abstract method")  # pragma: no cover

    # ----------------------------------------------------------------------
    # |
    # |  Private Data
    # |
    # ----------------------------------------------------------------------
    _NAME_VALIDATION_EXPR                   = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")
