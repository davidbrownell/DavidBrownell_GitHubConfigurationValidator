# ----------------------------------------------------------------------
# |
# |  RequireLinearHistoryPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:47:07
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
    "RequireLinearHistory",
    PluginBase.ConfigurationType.BranchProtection,
    False,
    "--require-linear-history",
    "settings/branches",
    "Protect matching branches",
    "Require linear history",
    lambda configuration: configuration["required_linear_history"]["enabled"],
)
