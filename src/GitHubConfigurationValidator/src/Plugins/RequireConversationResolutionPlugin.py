# ----------------------------------------------------------------------
# |
# |  RequireConversationResolutionPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 15:42:33
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
    "RequireConversationResolution",
    PluginBase.ConfigurationType.BranchProtection,
    SemVer("0.1.0"),
    True,
    "--no-require-conversation-resolution",
    "settings/branches",
    "Protect matching branches",
    "Require conversation resolution before merging",
    lambda configuration: configuration["required_conversation_resolution"]["enabled"],
    rationale=textwrap.dedent(
        """\
        The default behavior is to require conversation resolution before merging a pull request.

        Reasons for this Default
        ------------------------
        - Conversation resolution is an important part of the development process.
        - Prevent the accidental merging of a pull request before changes associated with the comments have been made.

        Reasons to Override this Default
        --------------------------------
        <unknown>
        """,
    ),
)
