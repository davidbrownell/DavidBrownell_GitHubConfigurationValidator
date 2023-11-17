# ----------------------------------------------------------------------
# |
# |  DeleteHeadBranchesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 12:01:04
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
    "DeleteHeadBranches",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-delete-head-branches",
    "settings",
    "Pull Requests",
    "Automatically delete head branches",
    lambda configuration: configuration["delete_branch_on_merge"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to automatically delete head branches once they have been merged into the mainline branch.

        Reasons for this Default
        ------------------------
        - Long-lived branches make integration more difficult, as changes accumulate over time.

        Reasons to Override this Default
        --------------------------------
        - You support release branches and may want to merge changes from this release branch into the mainline branch
          (although, it is possible to workaround this issue by creating a pull request from a temporary branch that
          includes cherry-picked changes from the release branch).
        """,
    ),
)
