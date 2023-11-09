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

import textwrap

from typing import Any

import typer

from Common_Foundation.Types import overridemethod
from Common_FoundationEx.TyperEx import TypeDefinitionsType

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase


# ----------------------------------------------------------------------
class Plugin(PluginBase):
    # ----------------------------------------------------------------------
    @classmethod
    @overridemethod
    def GetInstantiationParameters(cls) -> TypeDefinitionsType:
        return {
            "default_branch": (str, typer.Option("main", "--default-branch", help="Expected name of the default branch.")),
        }

    # ----------------------------------------------------------------------
    def __init__(
        self,
        default_branch: str,
    ):
        super(Plugin, self).__init__(
            "DefaultBranch",
            PluginBase.ConfigurationType.Repository,
            "Validates that the default branch is named '{}'.".format(default_branch),
            textwrap.dedent(
                """\
                To set the default branch to 'main':

                    1) Visit `https://github.com/davidbrownell/{{repository}}/settings`
                    2) Locate the `Default branch` section
                    3) Ensure that the branch is named "{}"


                """,
            ).format(default_branch),
        )

        self.default_branch                 = default_branch

    # ----------------------------------------------------------------------
    @overridemethod
    def Validate(
        self,
        configuration: dict[str, Any],
    ) -> PluginBase.ValidateResultType:
        if configuration["default_branch"] != self.default_branch:
            return "The default branch is not set to '{}' ('{}').".format(
                self.default_branch,
                configuration["default_branch"],
            )

        return None
