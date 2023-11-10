# ----------------------------------------------------------------------
# |
# |  DismissStalePullRequestApprovalsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:49:10
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

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase
from GitHubConfigurationValidator.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType:
    settings = configuration.get("required_pull_request_reviews", None)
    if settings is None:
        return None

    return settings["dismiss_stale_reviews"]


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "DismissStalePullRequestApprovals",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-dismiss-stale-pull-request-approvals",
    "settings/branches",
    "Protect matching branches",
    "Dismiss stale pull request approvals when new commits are pushed",
    _GetValue,
)