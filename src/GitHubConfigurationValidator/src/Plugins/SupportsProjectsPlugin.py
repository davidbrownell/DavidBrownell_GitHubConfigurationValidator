# ----------------------------------------------------------------------
# |
# |  SupportsProjectsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 11:39:32
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
    "SupportsProjects",
    PluginBase.ConfigurationType.Repository,
    True,
    "--no-supports-projects",
    "settings",
    "Features",
    "Projects",
    lambda configuration: configuration["has_projects"],
    subject="Support for Projects",
)
