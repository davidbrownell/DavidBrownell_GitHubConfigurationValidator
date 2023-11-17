# ----------------------------------------------------------------------
# |
# |  RequirePullRequestsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:21:32
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
    "RequirePullRequests",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--no-require-pull-requests",
    "settings/branches",
    "Protect matching branches",
    "Require a pull request before merging",
    lambda configuration: "required_pull_request_reviews" in configuration,
    rationale=textwrap.dedent(
        """\
        The default behavior is to require pull requests before merging.

        Reasons for this Default
        ------------------------
        - Pull requests are an important part of the development process and prevent unwanted changes from
          making it into the mainline branch.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
