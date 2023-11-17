# ----------------------------------------------------------------------
# |
# |  SupportsIssuesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 10:20:31
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
    "SupportsIssues",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-supports-issues",
    "settings",
    "Features",
    "Issues",
    lambda configuration: configuration["has_issues"],
    subject="Support for Issues",
    rationale=textwrap.dedent(
        """\
        No rationale for this default.
        """,
    ),
)
