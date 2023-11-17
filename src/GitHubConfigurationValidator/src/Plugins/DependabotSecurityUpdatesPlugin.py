# ----------------------------------------------------------------------
# |
# |  DependabotSecurityUpdatesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 21:21:03
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

    return security_and_analysis["dependabot_security_updates"]["status"] == "enabled"


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "DependabotSecurityUpdates",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-dependabot-security-updates",
    "settings/security_analysis",
    "Dependabot",
    "Dependabot security updates",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        The default behavior is to enable Dependabot security updates.

        Reasons for this Default
        ------------------------
        - Increases the security of the repository by automatically applying security updates.

        Reasons to Override this Default
        --------------------------------
        - Dependabot security updates are not supported for the repository or by the organization.
        """,
    ),
)
