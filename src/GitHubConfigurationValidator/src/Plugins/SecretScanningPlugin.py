# ----------------------------------------------------------------------
# |
# |  SecretScanningPlugin.py
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

import textwrap

from typing import Any

from semantic_version import Version as SemVer

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

    return security_and_analysis["secret_scanning"]["status"] == "enabled"


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "SecretScanning",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-secret-scanning",
    "settings/security_analysis",
    "Secret scanning",
    "Secret scanning",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        The default behavior is to enable secret scanning.

        Reasons for this Default
        ------------------------
        - Secrets should not be checked into code.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
