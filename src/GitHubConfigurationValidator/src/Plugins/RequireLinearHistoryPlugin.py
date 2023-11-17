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

import textwrap

from typing import Type as PythonType

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin

from Plugins.RebaseMergeCommitPlugin import Plugin as RebaseMergeCommitPlugin
from Plugins.SquashMergeCommitPlugin import Plugin as SquashMergeCommitPlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "RequireLinearHistory",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    False,
    "--require-linear-history",
    "settings/branches",
    "Protect matching branches",
    "Require linear history",
    lambda configuration: configuration["required_linear_history"]["enabled"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to not require a linear history as this option is disabled when rebase
        merging and squash merging are disabled (which are the default validation settings).

        Reasons for this Default
        ------------------------
        - This option is disabled within the GitHub UX when rebase merging and squash merging are disabled
          (which are the default validation settings).

        Reasons to Override this Default
        --------------------------------
        - You have enabled rebase merging or squash merging
        """,
    ),
)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetDefaultSetting(
    plugin: PythonType,
) -> bool:
    instantiation_parameters = plugin.GetInstantiationParameters()

    assert len(instantiation_parameters) == 1, instantiation_parameters
    typer_option = next(iter(instantiation_parameters.values()))

    typer_option = typer_option[1]
    return typer_option.default


assert _GetDefaultSetting(RebaseMergeCommitPlugin) is False, RebaseMergeCommitPlugin
assert _GetDefaultSetting(SquashMergeCommitPlugin) is False, SquashMergeCommitPlugin
