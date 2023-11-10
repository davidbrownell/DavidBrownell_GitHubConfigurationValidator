# ----------------------------------------------------------------------
# |
# |  ProtectedBranchPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:08:05
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
    "ProtectedBranch",
    PluginBase.ConfigurationType.Branch,
    True,
    "--no-protected-branch",
    "settings/branches",
    "Branch protection rules",
    "protected",
    lambda configuration: configuration["protected"],
)
