# ----------------------------------------------------------------------
# |
# |  SecretScanningPushProtectionPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 09:33:20
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

from typing import Any

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType | bool:
    security_and_analysis = configuration.get("security_and_analysis", None)
    if security_and_analysis is None:
        return (
            PluginBase.MessageType.Warning,
            "'security_and_analysis' was not found in the results; please provide a GitHub Personal Access Token (PAT).",
        )

    return security_and_analysis["secret_scanning_push_protection"]["status"] == "enabled"


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "SecretScanningPushProtection",
    PluginBase.ConfigurationType.Repository,
    True,
    "--no-secret-scanning-push-protection",
    "settings/security_analysis",
    "Secret scanning",
    "Push protection",
    _GetValue,
    subject="Secret Scanning Push Protection",
)
