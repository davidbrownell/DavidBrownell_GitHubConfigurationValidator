# ----------------------------------------------------------------------
# |
# |  setup.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 12:40:32
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Setup for GitHubConfigurationValidator"""

import datetime
import os
import sys
import textwrap

from pathlib import Path

from cx_Freeze import setup, Executable

from Common_Foundation.ContextlibEx import ExitStack
from Common_Foundation import PathEx
from Common_Foundation.Shell.All import CurrentShell
from Common_Foundation import SubprocessEx


# ----------------------------------------------------------------------
_this_dir                                   = Path(__file__).parent
_name                                       = _this_dir.name

_initial_year                               = 2023  # pylint: disable=invalid-name


# ----------------------------------------------------------------------
sys.path.insert(0, str(PathEx.EnsureDir(_this_dir / "src" / "EntryPoint")))
with ExitStack(lambda: sys.path.pop(0)):
    # We have to import in this way to get the proper doc string from __main__.py
    import __main__ as GitHubConfigurationValidatorMain


# ----------------------------------------------------------------------
def _GetVersion() -> str:
    result = SubprocessEx.Run(
        'AutoSemVer{ext} --no-metadata --style AllMetadata --quiet'.format(
            ext=CurrentShell.script_extensions[0],
        ),
        cwd=_this_dir,
    )

    assert result.returncode == 0, result.output
    return result.output.strip()

_version = _GetVersion()  # pylint: disable=invalid-name
del _GetVersion


# ----------------------------------------------------------------------
# Create the year suffix
_year = datetime.datetime.now().year

if _year == _initial_year:
    _year_suffix = ""  # pylint: disable=invalid-name
else:
    if _year < 2100:
        _year = _year % 100

    _year_suffix = "-" + str(_year)  # pylint: disable=invalid-name


# ----------------------------------------------------------------------
include_files: list[tuple[str, str]] = []

for include_path, is_supported_file_func in [
    (Path("src/Plugins"), lambda filename: filename.suffix == ".py" and filename.stem != "__init__"),
    (Path("src/Configs"), lambda filename: True),
]:
    for child in include_path.iterdir():
        if not (child.is_file() and is_supported_file_func(child)):
            continue

        include_files.append(
            (
                str(child),
                str(Path(*child.parts[1:])),
            ),
        )

for root_str, directories, filenames in os.walk(Path("src/GitHubConfigurationValidatorLib")):
    root = Path(root_str)

    if root.parts[-1] == "TestFiles":
        continue

    for filename in filenames:
        fullpath = root / filename

        include_files.append(
            (
                str(fullpath),
                str(Path(*fullpath.parts[1:])),
            ),
        )


# ----------------------------------------------------------------------
setup(
    name=_name,
    version=_version,
    description=GitHubConfigurationValidatorMain.__doc__,
    executables=[
        Executable(
            PathEx.EnsureFile(_this_dir / "src" / "EntryPoint" / "__main__.py"),
            base=None,
            copyright=textwrap.dedent(
                """\
                Copyright David Brownell {year}{year_suffix}
                Distributed under the Boost Software License, Version 1.0. See
                copy at http://www.boost.org/LICENSE_1_0.txt.
                """,
            ).format(
                year=str(_initial_year),
                year_suffix=_year_suffix,
            ),
            # icon=<icon_filename>
            target_name=_name,
            # trademarks="",
        ),
    ],
    options={
        "build_exe": {
            "excludes": [
                "tcl",
                "tkinter",
            ],
            "no_compress": False,
            "optimize": 0,
            "packages": [
                "dateutil",
                "semantic_version",
            ],
            "include_files": include_files,
        },
    },
)
