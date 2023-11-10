# ----------------------------------------------------------------------
# |
# |  RequireCodeOwnerReviewsPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-10 14:56:33
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

from typing import Any, Optional

from GitHubConfigurationValidator.Plugin import Plugin as PluginBase
from GitHubConfigurationValidator.Impl.PluginImpl import CreateValuePlugin, Result


# ----------------------------------------------------------------------
def _GetValue(
    configuration: dict[str, Any],
) -> PluginBase.ValidateResultType | Result[Optional[bool]]:
    settings = configuration.get("required_pull_request_reviews", None)
    if settings is None:
        return Result(None)

    return Result(settings["require_code_owner_reviews"])


# ----------------------------------------------------------------------
Plugin = CreateValuePlugin(
    "RequireCodeOwnerReviews",
    PluginBase.ConfigurationType.BranchProtection,
    True,
    "--no-require-code-owner-reviews",
    "settings/branches",
    "Protect matching branches",
    "Require review from Code Owners",
    _GetValue,
)
