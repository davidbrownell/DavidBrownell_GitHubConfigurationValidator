# ----------------------------------------------------------------------
# |
# |  Binary_BuildVerificationTest.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 15:19:12
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Build verification test for binaries"""

# Note that this file will be invoked outside of an activated environment and cannot take a dependency
# on anything in this repository or Common_Foundation.

import subprocess
import stat
import sys
import textwrap

from pathlib import Path


# ----------------------------------------------------------------------
def EntryPoint(
    args: list[str],
) -> int:
    if len(args) != 2:
        sys.stdout.write(
            textwrap.dedent(
                """\
                ERROR: Usage:

                    {} <temp_directory>

                """,
            ).format(
                args[0],
            ),
        )

        return -1

    temp_directory = Path(args[1])
    assert temp_directory.is_dir(), temp_directory

    # Get the binary
    binary_filename = Path(temp_directory) / "GitHubConfigurationValidator"

    if not binary_filename.is_file():
        potential_binary_filename = binary_filename.with_suffix(".exe")

        if potential_binary_filename.is_file():
            binary_filename = potential_binary_filename

    if not binary_filename.is_file():
        raise Exception("The filename '{}' does not exist.\n".format(binary_filename))

    # https://github.com/actions/upload-artifact/issues/38
    # Permissions are not currently being saved when uploading artifacts, so they must be set here.
    # This will eventually be fixed, which is why I am placing the work around here rather than in
    # the artifact upload- or download-code.
    binary_filename.chmod(stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    # Execute tests
    result = _RunTests(binary_filename)
    if result != 0:
        return result

    return 0


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _RunTests(
    binary_filename: Path,
) -> int:
    command_line = '"{binary}" ListPlugins'.format(
        binary=binary_filename,
    )

    sys.stdout.write("Command Line: {}\n\n".format(command_line))

    result = subprocess.run(
        command_line,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    content = result.stdout.decode("utf-8")

    sys.stdout.write(content)

    if not (
        "AutoMerge" in content
        and "DefaultBranch" in content
    ):
        return -1

    return 0


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(EntryPoint(sys.argv))
