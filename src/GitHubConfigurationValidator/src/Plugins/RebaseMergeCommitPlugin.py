# ----------------------------------------------------------------------
# |
# |  RebaseMergeCommitPlugin.py
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

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RebaseMergeCommit",
    PluginBase.ConfigurationType.Repository,
    False,
    "--rebase-merge-commit",
    "settings",
    "Pull Requests",
    "Allow rebase merging",
    lambda configuration: configuration["allow_rebase_merge"],
)
