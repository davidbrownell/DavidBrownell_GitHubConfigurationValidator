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

import os
import uuid                                             # pylint: disable=unused-import

from pathlib import Path
from typing import Optional, Union

from semantic_version import Version as SemVer          # pylint: disable=unused-import

from Common_Foundation import PathEx                                        # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Shell.All import CurrentShell                        # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Shell import Commands                                # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Streams.DoneManager import DoneManager               # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation import Types                                         # type: ignore  # pylint: disable=import-error,unused-import

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

    common_python_packages: list[Configuration.VersionInfo] = [
        Configuration.VersionInfo("typer-config", SemVer("1.2.1")),
    ]

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
            {                               # libraries
                "Python": common_python_packages + [
                    Configuration.VersionInfo("cx_freeze", SemVer("6.13.1")),
                ],
            },
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
            {                               # libraries
                "Python": common_python_packages,
            },
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

    commands: list[Commands.Command] = []

    root_dir = Path(__file__).parent
    assert root_dir.is_dir(), root_dir

    # Create a link to the foundation's .pylintrc file
    foundation_root_file = Path(Types.EnsureValid(os.getenv(Constants.DE_FOUNDATION_ROOT_NAME))) / ".pylintrc"
    assert foundation_root_file.is_file(), foundation_root_file

    commands.append(
        Commands.SymbolicLink(
            root_dir / foundation_root_file.name,
            foundation_root_file,
            remove_existing=True,
            relative_path=True,
        ),
    )

    # Create a link to __main__.py in Scripts
    commands.append(
        Commands.SymbolicLink(
            PathEx.EnsureDir(root_dir / "Scripts") / "GitHubConfigurationValidator.py",
            PathEx.EnsureFile(root_dir / "src" / "GitHubConfigurationValidator" / "src" / "EntryPoint" / "__main__.py"),
            remove_existing=True,
            relative_path=True,
        ),
    )

    return commands
