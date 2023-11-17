# ----------------------------------------------------------------------
# |
# |  RequireCodeOwnerReviewsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:56:33
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
) -> PluginBase.ValidateResultType | Result[Optional[int]]:
    settings = configuration.get("required_pull_request_reviews", None)
    if settings is None:
        return Result(None)

    return Result(settings["require_code_owner_reviews"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "RequireCodeOwnerReviews",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    1,
    "--require-code-owner-reviews",
    "settings/branches",
    "Protect matching branches",
    "Require review from Code Owners",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        The default behavior is to require at least one approval from a Code Owner.

        Reasons for this Default
        ------------------------
        - Code Reviews are a generally accepted best practice for software development.
        - The code is complex enough to require a review from a person knowledgeable about the code impacted by the pull request.

        Reasons to Override this Default
        --------------------------------
        - You are the only person working on the repository (set the value to 0).
        - You want to require more than one approval (set the value to the number of approvals required).
        - You are not comfortable with the amount of time code reviews introduce in the development process (set the value to 0).
        - Code can be reviewed by any member of the team (set the value to 0).
        """,
    ),
)
