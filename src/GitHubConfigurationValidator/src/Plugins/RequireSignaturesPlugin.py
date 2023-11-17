# ----------------------------------------------------------------------
# |
# |  RequireSignaturesPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:45:19
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
    "RequireSignatures",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--no-require-signatures",
    "settings/branches",
    "Protect matching branches",
    "Require signed commits",
    lambda configuration: configuration["required_signatures"]["enabled"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to require signed commits. Note that this setting does not work with
        rebase merging or squash merging.

        Reasons for this Default
        ------------------------
        - Ensure that the author of a commit is who the claim to be.

        Reasons to Override this Default
        --------------------------------
        - You have enabled rebase merging or squash merging.
        """,
    ),
)
