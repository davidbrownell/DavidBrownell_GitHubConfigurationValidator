# ----------------------------------------------------------------------
# |
# |  AllowBypassSettingsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:54:20
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

from semantic_version import Version as SemVer

from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase
from GitHubConfigurationValidatorLib.Impl.PluginImpl import CreateEnablePlugin


# ----------------------------------------------------------------------
Plugin = CreateEnablePlugin(
    "AllowBypassSettings",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--allow-bypass-settings",
    "settings/branches",
    "Protect matching branches",
    "Do not allow bypassing the above settings",
    lambda configuration: configuration["enforce_admins"]["enabled"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to not allow administrators to bypass branch protection settings.

            Reasons for this Default
            ------------------------
            - Ensure that all pull requests go through the same verification process.

            Reasons to Override this Default
            --------------------------------
            - The steps invoked during the verification process...
                * ...are unreliable.
                * ...take an excessive amount of time to complete.

            * Note that all of the reasons in this section are workarounds to address the underlying instability
              of the steps invoked during the verification process. The ideal solution is to address the
              underlying instability.
        """,
    ),
)
