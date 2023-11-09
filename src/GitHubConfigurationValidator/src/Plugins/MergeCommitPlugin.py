# ----------------------------------------------------------------------
# |
# |  MergeCommitPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:54:50
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
    "MergeCommit",
    PluginBase.ConfigurationType.Repository,
    "merge_commit",
    True,
    "--no-merge-commit",
    "settings",
    "Pull Requests",
    "Allow merge commits",
    lambda configuration: configuration["allow_merge_commit"],
)
