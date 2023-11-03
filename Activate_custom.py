# ----------------------------------------------------------------------
# |
# |  Activate_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 08:26:10
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

from pathlib import Path
from typing import Optional

from Common_Foundation.Shell import Commands                                # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Shell.All import CurrentShell                        # type: ignore  # pylint: disable=import-error,unused-import
from Common_Foundation.Streams.DoneManager import DoneManager               # type: ignore  # pylint: disable=import-error,unused-import

from RepositoryBootstrap import Configuration                               # type: ignore  # pylint: disable=import-error,unused-import
from RepositoryBootstrap import DataTypes                                   # type: ignore  # pylint: disable=import-error,unused-import


# ----------------------------------------------------------------------
# Note that it is safe to remove this function if it will never be used.
def GetCustomActions(                                                       # pylint: disable=too-many-arguments
    # Note that it is safe to remove any parameters that are not used
    dm: DoneManager,                                                        # pylint: disable=unused-argument
    repositories: list[DataTypes.ConfiguredRepoDataWithPath],               # pylint: disable=unused-argument
    generated_dir: Path,                                                    # pylint: disable=unused-argument
    configuration: Optional[str],                                           # pylint: disable=unused-argument
    version_specs: Configuration.VersionSpecs,                              # pylint: disable=unused-argument
    force: bool,                                                            # pylint: disable=unused-argument
    is_mixin_repo: bool,                                                    # pylint: disable=unused-argument
) -> list[Commands.Command]:
    """Returns a list of actions that should be invoked as part of the activation process."""

    return []
