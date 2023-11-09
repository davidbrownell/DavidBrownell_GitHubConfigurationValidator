# ----------------------------------------------------------------------
# |
# |  SuggestUpdatingPullRequestBranchesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 12:04:51
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

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase
from GitHubConfigurationValidator.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "SuggestUpdatingPullRequestBranches",
    PluginBase.ConfigurationType.Repository,
    "suggest_updating_pull_request_branches",
    True,
    "--no-suggest-updating-pull-request-branches",
    "settings",
    "Pull Requests",
    "Always suggest updating pull request branches",
    lambda configuration: configuration["allow_update_branch"],
)
