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

from typing import Any, Optional

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
    "PR_BODY",
    "--merge-commit-message",
    "settings",
    "Pull Requests",
    "Allow merge commits -> Default...",
    _GetValue,
)
