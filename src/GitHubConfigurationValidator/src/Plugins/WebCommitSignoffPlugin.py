# ----------------------------------------------------------------------
# |
# |  WebCommitSignoffPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:50:23
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
    "WebCommitSignoff",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    True,
    "--no-web-commit-signoff",
    "settings",
    "General",
    "Require contributors to sign off on web-based commits",
    lambda configuration: configuration["web_commit_signoff_required"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to require contributors to sign off on web-based commits.

        Reasons for this Default
        ------------------------
        - All changes (regardless of where they were made) should go through the same validation process.

        Reasons to Override this Default
        --------------------------------
        - Changes made via the web interface are considered to be benign and should not be subject to
          the standard validation process.
        """,
    ),
)
