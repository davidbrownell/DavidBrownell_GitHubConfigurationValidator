# ----------------------------------------------------------------------
# |
# |  MergeCommitMessagePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 12:43:31
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
    if not configuration["allow_merge_commit"]:
        return None

    return Result(configuration["merge_commit_message"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "MergeCommitMessage",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    "BLANK",
    "--merge-commit-message",
    "settings",
    "Pull Requests",
    "Allow merge commits -> Default...",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        Available values:

            PR_TITLE [Default message]
                Pull Request number and head branch on the first line; pull request title on the third line

            BLANK [Default to pull request title]
                Pull Request title and number on the first line.

            PR_BODY [Default to pull request title and description]
                Pull Request title and number on the first line; pull request description starting on the third line.

        The default setting is BLANK.

        Reasons for this Default
        ------------------------
        - Reduce redundant information by only duplicating the title of the commit(s).
        - PR_TITLE includes the head branch name, which oftentimes is not relevant information to preserve over time.
        - PR_BODY duplicates the title and description of the commit(s).

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
