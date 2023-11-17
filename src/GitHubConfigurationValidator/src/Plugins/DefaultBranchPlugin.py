# ----------------------------------------------------------------------
# |
# |  DefaultBranchPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 21:25:47
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
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateValuePlugin, Result


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "DefaultBranch",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    "main",
    "--default-branch",
    "settings",
    "Default Branch",
    None,
    lambda configuration: Result(configuration["default_branch"]),
    rationale=textwrap.dedent(
        """\
        The default behavior is not name the mainline/base/default branch "main".

        Reasons for this Default
        ------------------------
        - Eliminate divisive language in favor of non-divisive language, this includes eliminating
          the use of terms that were inappropriately and offensively taken from slavery including
          the elimination of the term master in favor of main.

          https://www.linkedin.com/pulse/technology-notes-how-tos-infrastructure-git-master-main-eldritch/

        Reasons to Override this Default
        --------------------------------
        - You are validating a legacy repository that still uses 'master' as the mainline/base/default branch.
        """,
    ),
)
