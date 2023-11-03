# ----------------------------------------------------------------------
# |
# |  Setup_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 08:25:39
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring

import uuid                                             # pylint: disable=unused-import

from typing import Optional, Union

from semantic_version import Version as SemVer          # pylint: disable=unused-import

from Common_Foundation.Shell.All import CurrentShell                        # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Shell import Commands                                # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Streams.DoneManager import DoneManager               # type: ignore  # pylint: disable=import-error,unused-import

from RepositoryBootstrap import Configuration                               # type: ignore  # pylint: disable=import-error,unused-import
from RepositoryBootstrap import Constants                                   # type: ignore  # pylint: disable=import-error,unused-import


def GetConfigurations() -> Union[
    Configuration.Configuration,
    dict[
        str,                                # configuration name
        Configuration.Configuration,
    ],
]:
    """Return configuration information for the repository"""

    d: dict[str, Configuration.Configuration] = {}

    d["dev"] = Configuration.Configuration(
        "Configuration to use when developing the tool.",
        [
            Configuration.Dependency(
                uuid.UUID("e4170a9d-70f9-4615-85b6-d514055e62b6"),
                "Common_PythonDevelopment",
                "python310",
                "https://github.com/davidbrownell/v4-CV_PythonDevelopment.git",
            ),
        ],
        Configuration.VersionSpecs(
            [],                             # tools
            {},                             # libraries
        ),
    )

    d["standard"] = Configuration.Configuration(
        "Configuration to use when running the tool.",
        [
            Configuration.Dependency(
                Constants.COMMON_FOUNDATION_REPOSITORY_ID,
                "Common_Foundation",
                "python310",
                "https://github.com/davidbrownell/v4-Common_Foundation.git",
            ),
        ],
        Configuration.VersionSpecs(
            [],                             # tools
            {},                             # libraries
        ),
    )

    return d


# ----------------------------------------------------------------------
# Note that it is safe to remove this function if it will never be used.
def GetCustomActions(
    # Note that it is safe to remove any parameters that are not used
    dm: DoneManager,                                    # pylint: disable=unused-argument
    explicit_configurations: Optional[list[str]],       # pylint: disable=unused-argument
    force: bool,                                        # pylint: disable=unused-argument
    interactive: Optional[bool],                        # pylint: disable=unused-argument
) -> list[Commands.Command]:
    """Return custom actions invoked as part of the setup process for this repository"""

    return []
