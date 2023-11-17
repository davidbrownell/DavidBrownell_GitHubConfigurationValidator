# ----------------------------------------------------------------------
# |
# |  SquashMergeCommitPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:52:25
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
    "SquashCommitMerge",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    False,
    "--squash-merge-commit",
    "settings",
    "Pull Requests",
    "Allow squash merging",
    lambda configuration: configuration["allow_squash_merge"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to not allow squash merging.

        Reasons for this Default
        ------------------------
        - Rebase merging is not compatible with signed commits, as GitHub creates a new commit when squashing.

        Reasons to Override this Default
        --------------------------------
        - Your repository does not require signatures.
        - You want to ensure that single-commit-changes are merged into the mainline branch to simplify the branch's history.
        """,
    ),
)
