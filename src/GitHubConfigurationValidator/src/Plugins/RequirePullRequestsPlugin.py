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

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RequirePullRequests",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-require-pull-requests",
    "settings/branches",
    "Protect matching branches",
    "Require a pull request before merging",
    lambda configuration: "required_pull_request_reviews" in configuration,
)
