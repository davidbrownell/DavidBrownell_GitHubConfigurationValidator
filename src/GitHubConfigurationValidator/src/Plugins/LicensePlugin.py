# ----------------------------------------------------------------------
# |
# |  LicensePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 13:12:24
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

from typing import Any, Optional

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateValuePlugin, Result


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType | Result[Optional[str]]:
    if configuration["license"] is None:
        return Result(None)

    return Result(configuration["license"]["name"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "License",
    PluginBase.ConfigurationType.Repository,
    "null",
    "--license",
    "settings",
    None,
    None,
    _GetValue,
)
