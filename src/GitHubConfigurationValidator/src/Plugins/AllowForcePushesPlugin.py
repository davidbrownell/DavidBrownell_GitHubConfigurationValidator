# ----------------------------------------------------------------------
# |
# |  AllowForcePushesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:56:59
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
    "AllowForcePushes",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    False,
    "--allow-force-pushes",
    "settings/branches",
    "Rules applied to everyone including administrators",
    "Allow force pushes",
    lambda configuration: configuration["allow_force_pushes"]["enabled"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to not allow force pushes to the mainline branch.

        Reasons for this Default
        ------------------------
        - Force pushes rewrite history, which break git lineage for all other clones of the repository.
          Merges are possible when this happens, but they are difficult to perform and data loss is
          possible.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
