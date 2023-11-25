# ----------------------------------------------------------------------
# |
# |  SquashMergeCommitMessagePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 13:03:03
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

from typing import Any, Optional

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateValuePlugin, Result


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType | Result[Optional[str]]:
    if not configuration["allow_squash_merge"]:
        return None

    return Result(configuration["squash_merge_commit_message"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "SquashMergeCommitMessage",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    "COMMIT_MESSAGES",
    "--squash-merge-commit-message",
    "settings",
    "Pull Requests",
    "Allow squash merging -> Default...",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        Available values:

            BLANK [Default to pull request title]
                Pull Request title and number on the first line.

            COMMIT_MESSAGES [Default to pull request title and commit details]
                Commit title and...
                    [Single Commit] ...commit message
                    [Multiple Commits] ...pull request title and number and list of commits

            PR_BODY [Default to pull request title and description]
                Pull Request title and number on the first line; commit description starting on the third line.

        The default setting is COMMIT_MESSAGES.

        Reasons for this Default
        ------------------------
        - Preserves the information in the original commits.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
