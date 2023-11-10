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

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase
from GitHubConfigurationValidator.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RequireStatusChecksToPass",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-require-status-checks-to-pass",
    "settings/branches",
    "Protect matching branches",
    "Require status checks to pass before merging",
    lambda configuration: configuration.get("required_status_checks", None) is not None,
)
