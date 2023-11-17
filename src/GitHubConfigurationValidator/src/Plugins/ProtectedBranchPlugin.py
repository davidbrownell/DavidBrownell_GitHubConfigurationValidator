# ----------------------------------------------------------------------
# |
# |  ProtectedBranchPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:08:05
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
    "ProtectedBranch",
    PluginBase.ConfigurationType.Branch,
    SemVer("0.1.0"),
    True,
    "--no-protected-branch",
    "settings/branches",
    "Branch protection rules",
    "protected",
    lambda configuration: configuration["protected"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to protect the mainline branch.

        Reasons for this Default
        ------------------------
        - The mainline branch is the most important branch in a repository and should be protected.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
