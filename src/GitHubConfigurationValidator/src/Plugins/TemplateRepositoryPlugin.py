# ----------------------------------------------------------------------
# |
# |  TemplateRepositoryPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 12:24:06
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

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "TemplateRepository",
    PluginBase.ConfigurationType.Repository,
    SemVer("0.1.0"),
    False,
    "--template-repository",
    "settings",
    "General",
    "Template repository",
    lambda configuration: configuration["is_template"],
)
