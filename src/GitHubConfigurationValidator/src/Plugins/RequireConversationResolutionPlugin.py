# ----------------------------------------------------------------------
# |
# |  RequireConversationResolutionPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:42:33
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
    "RequireConversationResolution",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-require-conversation-resolution",
    "settings/branches",
    "Protect matching branches",
    "Require conversation resolution before merging",
    lambda configuration: configuration["required_conversation_resolution"]["enabled"],
)
