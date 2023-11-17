# ----------------------------------------------------------------------
# |
# |  RequireApprovalsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:27:15
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

    return Result(settings["required_approving_review_count"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "RequireApprovals",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    1,
    "--require-approvals",
    "settings/branches",
    "Protected machine branches",
    "Require approvals",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        The default behavior is to require at least one approval.

        Reasons for this Default
        ------------------------
        - Code Reviews are a generally accepted best practice for software development.

        Reasons to Override this Default
        --------------------------------
        - You are the only person working on the repository (set the value to 0).
        - You want to require more than one approval (set the value to the number of approvals required).
        - You are not comfortable with the amount of time code reviews introduce in the development process (set the value to 0).
        """,
    ),
)
