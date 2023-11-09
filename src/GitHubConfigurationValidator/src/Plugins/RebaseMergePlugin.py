# ----------------------------------------------------------------------
# |
# |  RebaseMergePlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:57:47
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
    "RebaseMerge",
    PluginBase.ConfigurationType.Repository,
    "rebase_merge",
    False,
    "--rebase-merge",
    "settings",
    "Pull Requests",
    "Allow rebase merging",
    lambda configuration: configuration["allow_rebase_merge"],
)
