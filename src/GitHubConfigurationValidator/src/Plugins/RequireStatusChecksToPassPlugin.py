# ----------------------------------------------------------------------
# |
# |  RequireStatusChecksToPassPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:24:25
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
    "RequireStatusChecksToPass",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--no-require-status-checks-to-pass",
    "settings/branches",
    "Protect matching branches",
    "Require status checks to pass before merging",
    lambda configuration: configuration.get("required_status_checks", None) is not None,
    rationale=textwrap.dedent(
        """\
        The default behavior is to require status checks to pass before merging a pull request.

        Reasons for this Default
        ------------------------
        - Status checks are an important part of the development process and should not be bypassed.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
