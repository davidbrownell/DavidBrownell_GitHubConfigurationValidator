# ----------------------------------------------------------------------
# |
# |  RequireLastPushApprovalsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:04:29
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
    settings = configuration.get("required_pull_request_reviews", None)
    if settings is None:
        return None

    return settings["require_last_push_approval"]


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RequireLastPushApprovals",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-require-last-push-approvals",
    "settings/branches",
    "Protect matching branches",
    "Require approval of the most recent reviewable push",
    _GetValue,
)
