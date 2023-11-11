# ----------------------------------------------------------------------
# |
# |  AllowDeletionsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:58:53
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
    "AllowDeletions",
    PluginBase.ConfigurationType.BranchProtection,
    False,
    "--allow-deletions",
    "settings/branches",
    "Rules applied to everyone including administrators",
    "Allow deletions",
    lambda configuration: configuration["allow_deletions"]["enabled"],
)
