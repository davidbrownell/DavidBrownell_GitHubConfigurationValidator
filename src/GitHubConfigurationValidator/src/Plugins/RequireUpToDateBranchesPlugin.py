# ----------------------------------------------------------------------
# |
# |  RequireUpToDateBranchesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:34:52
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

from typing import Any

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType | bool:
    settings = configuration.get("required_status_checks", None)
    if settings is None:
        return None

    return settings["strict"]


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RequireUpToDateBranches",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--no-require-up-to-date-branches",
    "settings/branches",
    "Protect matching branches",
    "Require status checks to pass before merging -> Require branches to be up to date before merging",
    _GetValue,
    rationale=textwrap.dedent(
        """\
        The default behavior is to require branches to be up to date before merging. The terminology
        used by GitHub is a bit confusing, as this setting ensure that all GitHub workflows triggered
        by the pull request have completed successfully before the pull request can be merged.

        Reasons for this Default
        ------------------------
        - Workflows run should pass before a pull request is merged into the mainline branch.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
