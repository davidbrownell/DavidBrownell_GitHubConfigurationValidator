# ----------------------------------------------------------------------
# |
# |  AutoMergePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:59:30
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
    "AutoMerge",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-auto-merge",
    "settings",
    "Pull Requests",
    "Allow auto-merge",
    lambda configuration: configuration["allow_auto_merge"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to enable the option to auto-merge once all the required status checks associated with a pull request have passed.

        Reasons for this Default
        ------------------------
        - Reduces mean resolution time by triggering the merge once all require status checks pass.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
