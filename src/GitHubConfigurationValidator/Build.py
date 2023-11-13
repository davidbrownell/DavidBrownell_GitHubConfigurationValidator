# ----------------------------------------------------------------------
# |
# |  Build.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-09 12:39:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Builds GitHubConfigurationValidator"""

import re
import textwrap
import uuid

from pathlib import Path
from typing import Callable, Optional, TextIO, Tuple, Union

from Common_Foundation.ContextlibEx import ExitStack
from Common_Foundation import PathEx
from Common_Foundation.Shell.All import CurrentShell
from Common_Foundation.Streams.DoneManager import DoneManager, DoneManagerFlags
from Common_Foundation import SubprocessEx
from Common_Foundation.Types import overridemethod

from Common_FoundationEx.BuildImpl import BuildInfoBase
from Common_FoundationEx import TyperEx

try:
    from Common_PythonDevelopment.BuildPythonExecutable import Build, BuildSteps, Clean

    clean_func = Clean
    build_func = Build

except ModuleNotFoundError:
    # ----------------------------------------------------------------------
    def CleanImpl(*args, **kwargs):  # pylint: disable=unused-argument
        return 0

    # ----------------------------------------------------------------------
    def BuildImpl(*args, **kwargs):  # pylint: disable=unused-argument
        return 0

    # ----------------------------------------------------------------------

    clean_func = CleanImpl
    build_func = BuildImpl


# ----------------------------------------------------------------------
class BuildInfo(BuildInfoBase):
    # ----------------------------------------------------------------------
    def __init__(self):
        super(BuildInfo, self).__init__(
            name="GitHubConfigurationValidator",
            requires_output_dir=True,
            required_development_configurations=[
                re.compile("dev"),
            ],
            disable_if_dependency_environment=True,
        )

    # ----------------------------------------------------------------------
    @overridemethod
    def Clean(                              # pylint: disable=arguments-differ
        self,
        configuration: Optional[str],       # pylint: disable=unused-argument
        output_dir: Path,
        output_stream: TextIO,
        on_progress_update: Callable[       # pylint: disable=unused-argument
            [
                int,                        # Step ID
                str,                        # Status info
            ],
            bool,                           # True to continue, False to terminate
        ],
        *,
        is_verbose: bool,
        is_debug: bool,
    ) -> Union[
        int,                                # Error code
        Tuple[int, str],                    # Error code and short text that provides info about the result
    ]:
        return clean_func(
            output_dir,
            output_stream,
            is_verbose=is_verbose,
            is_debug=is_debug,
        )

    # ----------------------------------------------------------------------
    @overridemethod
    def GetCustomBuildArgs(self) -> TyperEx.TypeDefinitionsType:
        """Return argument descriptions for any custom args that can be passed to the Build func on the command line"""

        # No custom args by default
        return {}

    # ----------------------------------------------------------------------
    @overridemethod
    def GetNumBuildSteps(
        self,
        configuration: Optional[str],  # pylint: disable=unused-argument
    ) -> int:
        return len(BuildSteps)

    # ----------------------------------------------------------------------
    @overridemethod
    def Build(                              # pylint: disable=arguments-differ
        self,
        configuration: Optional[str],       # pylint: disable=unused-argument
        output_dir: Path,
        output_stream: TextIO,
        on_progress_update: Callable[       # pylint: disable=unused-argument
            [
                int,                        # Step ID
                str,                        # Status info
            ],
            bool,                           # True to continue, False to terminate
        ],
        *,
        is_verbose: bool,
        is_debug: bool,
        force: bool=False,
    ) -> Union[
        int,                                # Error code
        Tuple[int, str],                    # Error code and short text that provides info about the result
    ]:
        return build_func(
            output_dir,
            output_stream,
            on_progress_update,
            is_verbose=is_verbose,
            is_debug=is_debug,
            force=force,
        )


# ----------------------------------------------------------------------
def CreateDockerImage(
    docker_image_name: str=TyperEx.typer.Argument(..., help="Name of the docker image to create."),
    docker_base_image: str=TyperEx.typer.Option("ubuntu:latest", "--base-image", help="Name of the docker image used as a base for the created image; the value will be extracted from the binary name if not provided on the command line."),
    force: bool=TyperEx.typer.Option(False, "--force", help="Force the (re)generation of layers within the image."),
    no_squash: bool=TyperEx.typer.Option(False, "--no-squash", help="Do not squash layers within the image."),
    verbose: bool=TyperEx.typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=TyperEx.typer.Option(False, "--verbose", help="Write debug information to the terminal."),
) -> int:
    """Creates a docker image that can be used to run GitHubConfigurationValidator without installing all python dependencies."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        source_root = PathEx.EnsureDir(Path(__file__).parent)
        repo_root = PathEx.EnsureDir(source_root.parent.parent)

        assert source_root != repo_root, (source_root, repo_root)

        working_dir = CurrentShell.CreateTempDirectory()
        with ExitStack(lambda: PathEx.RemoveTree(working_dir)):
            unique_id = str(uuid.uuid4()).replace("-", "")

            # Calculate the current version
            version: Optional[str] = None

            with dm.Nested("Calculating version...", lambda: version):
                result = SubprocessEx.Run(
                    "AutoSemVer{} --no-metadata --no-branch-name --quiet".format(CurrentShell.script_extensions[0]),
                    cwd=source_root,
                )

                assert result.returncode == 0, result
                version = result.output.strip()

            # Create the docker file used to build the binary
            docker_filename = working_dir / "Dockerfile"
            archive_name = "GitHubConfigurationValidator-{}-{}.tgz".format(version, docker_base_image.split(":")[0])

            with dm.Nested("Creating the archive dockerfile..."):
                # Remove the local build directory (if it exists), as we don't want it to be copied to the docker image
                PathEx.RemoveTree(Path(__file__).parent / "build")

                with docker_filename.open("w") as f:
                    f.write(
                        textwrap.dedent(
                            """\
                            FROM {base_image}

                            # Note that these instructions assume a debian-based distribution
                            RUN apt update && apt install -y git

                            RUN mkdir code
                            WORKDIR /code

                            COPY . .

                            RUN bash -c "./Bootstrap.sh /tmp/code_dependencies --debug"

                            RUN bash -c "source ./Activate.sh dev --debug \\
                                && cd src/GitHubConfigurationValidator \\
                                && python Build.py Build /tmp/GitHubConfigurationValidator --debug"

                            RUN bash -c "mkdir /tmp/GitHubConfigurationValidator_binary \\
                                && cd /tmp/GitHubConfigurationValidator \\
                                && tar -czvf /tmp/GitHubConfigurationValidator_binary/{archive_name} *"
                            """,
                        ).format(
                            base_image=docker_base_image,
                            archive_name=archive_name,
                        ),
                    )

            # Create the image that includes the built archive
            with dm.Nested("Building the archive via a docker image...") as build_dm:
                command_line = 'docker build --tag {tag} -f {dockerfile} .'.format(
                    tag=unique_id,
                    dockerfile=docker_filename,
                )

                build_dm.WriteVerbose("Command Line: {}\n\n".format(command_line))

                with build_dm.YieldStream() as stream:
                    build_dm.result = SubprocessEx.Stream(
                        command_line,
                        stream,
                        cwd=repo_root,
                    )

                    if build_dm.result != 0:
                        return build_dm.result

            # Extract the archive within the image
            with dm.Nested("Extracting the archive from the docker image...") as extract_dm:
                command_line = 'docker run --rm -v "{output_dir}:/local" {tag} bash -c "cp /tmp/GitHubConfigurationValidator_binary/* /local"'.format(
                    tag=unique_id,
                    output_dir=working_dir,
                )

                extract_dm.WriteVerbose("Command Line: {}\n\n".format(command_line))

                with extract_dm.YieldStream() as stream:
                    extract_dm.result = SubprocessEx.Stream(command_line, stream)

                    if extract_dm.result != 0:
                        return extract_dm.result

            # Remove the image
            with dm.Nested("Removing docker image...") as remove_dm:
                command_line = 'docker image rm {}'.format(unique_id)

                remove_dm.WriteVerbose("Command Line: {}\n\n".format(command_line))

                with remove_dm.YieldStream() as stream:
                    remove_dm.result = SubprocessEx.Stream(command_line, stream)

                    if remove_dm.result != 0:
                        return remove_dm.result

            # Create the execute dockerfile
            with dm.Nested("Creating the execute dockerfile..."):
                with docker_filename.open("w") as f:
                    f.write(
                        textwrap.dedent(
                            """\
                            FROM {base_image}

                            # Note that these instructions assume a debian-based distribution

                            RUN apt update \\
                                && rm -rf /var/lib/apt/lists/*

                                RUN mkdir GitHubConfigurationValidator
                                WORKDIR GitHubConfigurationValidator

                                COPY . .
                                RUN bash -c "tar -xvf {archive_name} \\
                                    && rm {archive_name}"

                                ENTRYPOINT ["./GitHubConfigurationValidator"]
                            """,
                        ).format(
                            base_image=docker_base_image,
                            archive_name=archive_name,
                        ),
                    )

            with dm.Nested("Building docker image...") as build_dm:
                command_line = 'docker build --tag {image_name} -f {dockerfile}{squash}{no_cache} .'.format(
                    image_name=docker_image_name,
                    dockerfile=docker_filename,
                    squash="" if no_squash else " --squash",
                    no_cache="" if force else " --no-cache",
                )

                build_dm.WriteVerbose("Command Line: {}\n\n".format(command_line))

                with build_dm.YieldStream() as stream:
                    build_dm.result = SubprocessEx.Stream(
                        command_line,
                        stream,
                        cwd=working_dir,
                    )

                    if build_dm.result != 0:
                        return build_dm.result

            with dm.Nested("Tagging image...") as tag_dm:
                command_line = 'docker tag {image_name}:latest {image_name}:{version}'.format(
                    image_name=docker_image_name,
                    version=version,
                )

                tag_dm.WriteVerbose("Command Line: {}\n\n".format(command_line))

                with tag_dm.YieldStream() as stream:
                    tag_dm.result = SubprocessEx.Stream(command_line, stream)

                    if tag_dm.result != 0:
                        return tag_dm.result

        return dm.result


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    BuildInfo().Run()
