# ----------------------------------------------------------------------
# |
# |  DefaultBranchPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 21:25:47
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
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateValuePlugin, Result


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "DefaultBranch",
    PluginBase.ConfigurationType.Repository,
    "main",
    "--default-branch",
    "settings",
    "Default Branch",
    None,
    lambda configuration: Result(configuration["default_branch"]),
)
