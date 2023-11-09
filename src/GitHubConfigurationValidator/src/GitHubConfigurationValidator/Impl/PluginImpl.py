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

from typing import Any, Callable, Optional, Type as PythonType
from Common_FoundationEx.TyperEx import TypeDefinitionsType

import typer

from Common_Foundation.Types import overridemethod

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase


# ----------------------------------------------------------------------
def CreateEnablePlugin(
    name: str,
    configuration_type: PluginBase.ConfigurationType,
    instantiation_parameter_name: str,
    instantiation_parameter_default_value: bool,
    instantiation_parameter_flag_name: str,
    github_settings_url_suffix: str,
    github_settings_section: str,
    github_settings_value: str,
    get_configuration_value_func: Callable[[dict[str, Any]], PluginBase.ValidateResultType | bool],
    subject: Optional[str]=None,
) -> PythonType:
    """Creates a Plugin class for plugins that check if a value is enabled or disabled."""

    if not subject:
        subject = github_settings_value

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
                        help="Indicates that '{}' should be {}.".format(
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
                "Validates that '{}' is {}.".format(subject, enable_desc),
                textwrap.dedent(
                    """\
                    1) Visit `{{repository}}/{github_settings_url_suffix}`
                    2) Locate the `{github_settings_section}` section
                    3) Ensure that `{github_settings_value}` is {checked_desc}
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

            if not isinstance(result, bool):
                return result

            if result != self._enable_value:
                return "'{}' is not {}.\n".format(subject, self._enable_desc)

            return None

    # ----------------------------------------------------------------------

    return Plugin
