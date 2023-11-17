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

import textwrap

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "SuggestUpdatingPullRequestBranches",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    False,
    "--suggest-updating-pull-request-branches",
    "settings",
    "Pull Requests",
    "Always suggest updating pull request branches",
    lambda configuration: configuration["allow_update_branch"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to not suggest updating branches associated with pull requests within the pull request.

        Reasons for this Default
        ------------------------
        - Pull requests updated by GitHub are not compatible with signed commits, as GitHub creates a new commit when rebasing.
        - Rebasing may introduce changes that are incompatible with the current pull request.

        Reasons to Override this Default
        --------------------------------
        - Your repository does not require signatures.
        - Merge problems more insidious than conflicts are infrequent.
        """,
    ),
)
