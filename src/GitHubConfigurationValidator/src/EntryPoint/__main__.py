# ----------------------------------------------------------------------
# |
# |  __main__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-03 08:48:43
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Tools that validates GitHub configuration settings."""

import importlib
import re
import sys
import textwrap

from io import StringIO
from pathlib import Path
from typing import Any, Callable, cast, Iterator, Optional, Pattern, Type as PythonType

import requests
import typer

from typer.core import TyperGroup
from typer_config.decorators import use_yaml_config

from Common_Foundation.ContextlibEx import ExitStack
from Common_Foundation import PathEx
from Common_Foundation.Shell.All import CurrentShell
from Common_Foundation.Streams.Capabilities import Capabilities
from Common_Foundation.Streams.DoneManager import DoneManager, DoneManagerException, DoneManagerFlags
from Common_Foundation import TextwrapEx

from Common_FoundationEx import ExecuteTasks
from Common_FoundationEx.InflectEx import inflect
from Common_FoundationEx.TyperEx import TypeDefinitionsType, ProcessDynamicArgs


# ----------------------------------------------------------------------
_root_dir = PathEx.EnsureDir(Path(__file__).parent.resolve())


# ----------------------------------------------------------------------
# This configuration (in terms of the items listed below) is the only way that I could get
# this to work both locally and when frozen as an executable, here and with plugins.
#
# Modify at your own risk.
#
#   Factors that contributed to this configuration:
#
#       - Directory name (which is why there is the funky 'src/GitHubConfigurationValidator/src/GitHubConfigurationValidator' layout
#       - This file as 'EntryPoint/__main__.py' rather than '../EntryPoint.py'
#       - Build.py/setup.py located outside of 'src'
#
sys.path.insert(0, str(PathEx.EnsureDir(_root_dir.parent)))
with ExitStack(lambda: sys.path.pop(0)):
    from GitHubConfigurationValidator.Plugin import Plugin


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
_DEFAULT_GITHUB_URL                         = "https://api.github.com"

# ----------------------------------------------------------------------
app                                         = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


_plugin_name_argument                       = typer.Argument(None, help="Name of the plugin. Run `ListsPlugins` to list all available plugins.")
_username_argument                          = typer.Argument(None, help="GitHub username or organization.")

_additional_plugin_dirs_option              = typer.Option(None, "--plugin-dir", file_okay=False, exists=True, help="Additional directories to search for plugins.")
_github_url_option                          = typer.Option(_DEFAULT_GITHUB_URL, "--github-url", help="GitHub url. ")
_pat_option                                 = typer.Option(None, "--pat", help="GitHub Personal Access Token (PAT) or filename containing a PAT.")
_ignore_archived_option                     = typer.Option(None, "--ignore-archived", help="Do not process archived repositories.")
_ignore_forks_option                        = typer.Option(None, "--ignore-forks", help="Do not process forked repositories.")
_include_repos_option                       = typer.Option(None, "--include-repo", help="Regular expression matching GitHub repository names that should be processed.")
_exclude_repos_option                       = typer.Option(None, "--exclude-repo", help="Regular expression matching GitHub repository names that should not be processed.")
_include_plugins_option                     = typer.Option(None, "--include-plugin", help="Regular expression matching plugin names that should be applied.")
_exclude_plugins_option                     = typer.Option(None, "--exclude-plugin", help="Regular expression matching plugin names that should not be applied.")


# ----------------------------------------------------------------------
@app.command(
    "ListPlugins",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    no_args_is_help=False,
)
@use_yaml_config()
def ListPlugins(
    ctx: typer.Context,
    additional_plugin_dirs: list[Path]=_additional_plugin_dirs_option,
    verbose: bool=typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=typer.Option(False, "--debug", help="Write debug information to the terminal."),
) -> None:
    """Lists all available Plugins."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        plugins = _GetPlugins(ctx, dm, additional_plugin_dirs, [], [])

        with dm.YieldStream() as stream:
            stream.write(
                TextwrapEx.CreateTable(
                    ["Name", "Description"],
                    [
                        [plugin.name, plugin.description]
                        for plugin in plugins
                    ],
                ),
            )

            stream.write("\n")


# ----------------------------------------------------------------------
@app.command(
    "PluginInfo",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    no_args_is_help=True,
)
@use_yaml_config()
def PluginInfo(
    ctx: typer.Context,
    plugin_name: str=_plugin_name_argument,
    additional_plugin_dirs: list[Path]=_additional_plugin_dirs_option,
    verbose: bool=typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=typer.Option(False, "--debug", help="Write debug information to the terminal."),
) -> None:
    """Displays information about a Plugin."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        plugins = _GetPlugins(ctx, dm, additional_plugin_dirs, [], [])

        plugin = next((plugin for plugin in plugins if plugin.name == plugin_name), None)
        if plugin is None:
            dm.WriteError("'{}' is not a recognized plugin.\n".format(plugin_name))
            return

        with dm.YieldStream() as stream:
            stream.write(
                textwrap.dedent(
                    """\
                    Name:                   {name}
                    Configuration Type:     {configuration_type}

                    Description
                    -----------
                    {description}

                    Resolution
                    ----------
                    {resolution}

                    """,
                ).format(
                    name=plugin.name,
                    configuration_type=plugin.configuration_type.name,
                    description=plugin.description,
                    resolution=plugin.resolution_description.format(
                        repository="<repo name here>",
                    ),
                ),
            )


# ----------------------------------------------------------------------
@app.command("ListRepos", no_args_is_help=True)
@use_yaml_config()
def ListRepos(
    username: str=_username_argument,
    github_url: str=_github_url_option,
    pat: str=_pat_option,
    ignore_archived: bool=_ignore_archived_option,
    ignore_forks: bool=_ignore_forks_option,
    include_repos: list[str]=_include_repos_option,
    exclude_repos: list[str]=_exclude_repos_option,
    verbose: bool=typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=typer.Option(False, "--debug", help="Write debug information to the terminal."),
) -> None:
    """Lists all repositories associated with a GitHub user/organization."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        session = _CustomSession(github_url, pat)

        repositories = _GetRepos(
            dm,
            session,
            username,
            include_repos,
            exclude_repos,
            ignore_archived=ignore_archived,
            ignore_forks=ignore_forks,
        )

        with dm.YieldStream() as stream:
            stream.write(
                "\n".join(
                    "{}) {}".format(index + 1, repository)
                    for index, repository in enumerate(repositories)
                ),
            )
            stream.write("\n")


# ----------------------------------------------------------------------
@app.command(
    "ValidateRepo",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    no_args_is_help=True,
)
@use_yaml_config()
def ValidateRepo(
    ctx: typer.Context,
    username: str=_username_argument,
    repository: str=typer.Argument(None, help="Name of the GitHub repository to validate."),
    github_url: str=_github_url_option,
    pat: str=_pat_option,
    include_plugins: list[str]=_include_plugins_option,
    exclude_plugins: list[str]=_exclude_plugins_option,
    additional_plugin_dirs: list[Path]=_additional_plugin_dirs_option,
    verbose: bool=typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=typer.Option(False, "--debug", help="Write debug information to the terminal."),
) -> None:
    """Validates a GitHub repository."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        _ValidateRepo(
            dm,
            _CustomSession(github_url, pat),
            username,
            repository,
            _GetPlugins(ctx, dm, additional_plugin_dirs, include_plugins, exclude_plugins),
        )


# ----------------------------------------------------------------------
@app.command(
    "ValidateRepos",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    no_args_is_help=True,
)
@use_yaml_config()
def ValidateRepos(
    ctx: typer.Context,
    username: str=_username_argument,
    github_url: str=_github_url_option,
    pat: str=_pat_option,
    ignore_archived: bool=_ignore_archived_option,
    ignore_forks: bool=_ignore_forks_option,
    include_repos: list[str]=_include_repos_option,
    exclude_repos: list[str]=_exclude_repos_option,
    include_plugins: list[str]=_include_plugins_option,
    exclude_plugins: list[str]=_exclude_plugins_option,
    additional_plugin_dirs: list[Path]=_additional_plugin_dirs_option,
    verbose: bool=typer.Option(False, "--verbose", help="Write verbose information to the terminal."),
    debug: bool=typer.Option(False, "--debug", help="Write debug information to the terminal."),
) -> None:
    """Validates repositories associated with a GitHub user/organization."""

    with DoneManager.CreateCommandLine(
        output_flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        plugins = _GetPlugins(ctx, dm, additional_plugin_dirs, include_plugins, exclude_plugins)

        session = _CustomSession(github_url, pat)

        repositories = _GetRepos(
            dm,
            session,
            username,
            include_repos,
            exclude_repos,
            ignore_archived=ignore_archived,
            ignore_forks=ignore_forks,
        )
        if not repositories:
            return

        # ----------------------------------------------------------------------
        def Execute(
            context: str,
            on_simple_status_func: Callable[[str], None],  # pylint: disable=unused-argument
        ) -> ExecuteTasks.TransformTypes.FuncType[Optional[str]]:
            repository = context
            del context

            # ----------------------------------------------------------------------
            def Impl(
                status: ExecuteTasks.Status,  # pylint: disable=unused-argument
            ) -> Optional[str]:
                sink = StringIO()

                Capabilities.Set(sink, dm.capabilities)

                with DoneManager.Create(
                    sink,
                    "Checking '{}'...".format(repository),
                ) as this_dm:
                    _ValidateRepo(
                        this_dm,
                        session,
                        username,
                        repository,
                        plugins,
                    )

                if this_dm.result != 0:
                    return sink.getvalue()

                return None

            # ----------------------------------------------------------------------

            return Impl

        # ----------------------------------------------------------------------

        results = ExecuteTasks.Transform(
            dm,
            "Validating repositories...",
            [
                ExecuteTasks.TaskData(repository, repository)
                for repository in repositories
            ],
            Execute,
        )

        dm.WriteLine("")

        for result in results:
            if result is not None:
                dm.WriteLine(cast(str, result))
                dm.WriteLine("")

                dm.result = -1


# ----------------------------------------------------------------------
# |
# |  Private Types
# |
# ----------------------------------------------------------------------
class _CustomSession(requests.Session):
    # ----------------------------------------------------------------------
    def __init__(
        self,
        github_url: str,
        pat: Optional[str],
        *args,
        **kwargs,
    ):
        super(_CustomSession, self).__init__(*args, **kwargs)

        if github_url.endswith("/"):
            github_url = github_url[:-1]

        self._github_url                    = github_url

        self.headers["X-GitHub-Api-Version"] = "2022-11-28"

        if pat:
            potential_file = Path(pat)

            if potential_file.is_file():
                with potential_file.open("r") as f:
                    pat = f.read().strip()

            self.headers["Authorization"] = "Bearer {}".format(pat)

        self.is_enterprise                  = self._github_url != _DEFAULT_GITHUB_URL
        self.has_pat                        = bool(pat)

    # ----------------------------------------------------------------------
    def request(self, method, url, *args, **kwargs):
        if not url.startswith("/"):
            url = "/{}".format(url)

        return super(_CustomSession, self).request(
            method,
            "{}{}".format(self._github_url, url),
            *args,
            **kwargs,
        )


# ----------------------------------------------------------------------
# |
# |  Private Functions
# |
# ----------------------------------------------------------------------
def _CreateRegexes(
    regexes: list[str],
) -> list[Pattern]:
    results: list[Pattern] = []

    for regex in regexes:
        if not regex.startswith("^"):
            regex = "^{}".format(regex)
        if not regex.endswith("$"):
            regex = "{}$".format(regex)

        try:
            results.append(re.compile(regex))
        except Exception as ex:
            raise DoneManagerException(
                "The regular expression '{}' is not valid: {}.".format(regex, ex),
            ) from ex

    return results


# ----------------------------------------------------------------------
def _GetPlugins(
    ctx: typer.Context,
    dm: DoneManager,
    additional_plugin_dirs: list[Path],
    include_plugins: list[str],
    exclude_plugins: list[str],
) -> list[Plugin]:
    include_plugin_regexes = _CreateRegexes(include_plugins)
    exclude_plugin_regexes = _CreateRegexes(exclude_plugins)

    del include_plugins
    del exclude_plugins

    plugin_dirs: list[Path] = []

    for potential_plugin_dir in [
        _root_dir / "Plugins",
        _root_dir.parent / "Plugins",
    ]:
        if potential_plugin_dir.is_dir():
            plugin_dirs.append(potential_plugin_dir)

    plugin_dirs += additional_plugin_dirs

    # There is a bit of the chicken-and-egg problem here. We need to know all of the
    # custom parameters across all plugins before we can parse the command line arguments
    # that correspond to the arguments, but then also need to instantiate the plugin using these
    # values. Here is what we do...
    #
    # 1) Walk all of the plugins and put together a dictionary of all the parameters.
    # 2) For each plugin with custom parameters, create a callback that instantiates the plugin with the command line values.
    # 3) Parse the arguments provided on the command line.
    # 4) Invoke each callback with the command line parameters to instantiate the Plugins that were deferred.

    # Get the plugins
    custom_parameter_types: TypeDefinitionsType = {}
    create_plugin_callback_funcs: list[Callable[[dict[str, Any]], Plugin]] = []

    plugins: list[Plugin] = []

    with dm.Nested(
        "Loading plugins from {}...".format(inflect.no("directory", len(plugin_dirs))),
        lambda: "{} found".format(inflect.no("plugin", len(plugins))),
        suffix="\n",
    ) as load_dm:
        for index, plugin_dir in enumerate(plugin_dirs):
            with load_dm.VerboseNested("Processing '{}' ({} of {})...".format(plugin_dir, index + 1, len(plugin_dirs))) as dir_dm:
                sys.path.insert(0, str(plugin_dir))
                with ExitStack(lambda: sys.path.pop(0)):
                    for filename in plugin_dir.iterdir():
                        if filename.suffix != ".py":
                            continue

                        if not filename.stem.endswith("Plugin"):
                            continue

                        if filename.stem == "Plugin":
                            continue

                        mod = importlib.import_module(filename.stem)

                        found_plugin = False

                        for potential_name in [
                            "Plugin",
                        ]:
                            potential_plugin = getattr(mod, potential_name, None)
                            if potential_plugin is None:
                                continue

                            found_plugin = True

                            parameters = potential_plugin.GetInstantiationParameters()

                            if not parameters:
                                create_plugin_callback_funcs.append(lambda arguments, plugin=potential_plugin: plugin())
                            else:
                                for k, v in parameters.items():
                                    assert k not in custom_parameter_types, k
                                    custom_parameter_types[k] = v

                                # ----------------------------------------------------------------------
                                def CreatePlugin(
                                    arguments: dict[str, Any],
                                    plugin: PythonType=potential_plugin,  # type: ignore
                                    parameters: TypeDefinitionsType=parameters,
                                ) -> Plugin:
                                    kwargs: dict[str, Any] = {}

                                    for k in parameters.keys():
                                        kwargs[k] = arguments[k]

                                    return plugin(**kwargs)

                                # ----------------------------------------------------------------------

                                create_plugin_callback_funcs.append(CreatePlugin)

                            break

                        if not found_plugin:
                            dir_dm.WriteInfo("A plugin class was not found in '{}'.\n".format(filename))

        if custom_parameter_types:
            arguments = ProcessDynamicArgs(ctx, custom_parameter_types)
        else:
            arguments = {}

        for create_plugin_func in create_plugin_callback_funcs:
            plugin = create_plugin_func(arguments)

            if exclude_plugin_regexes and any(expr.match(plugin.name) for expr in exclude_plugin_regexes):
                load_dm.WriteInfo("'{}' was excluded.\n".format(plugin.name))
                continue

            if include_plugin_regexes and not any(expr.match(plugin.name) for expr in include_plugin_regexes):
                load_dm.WriteInfo("'{}' was not included.\n".format(plugin.name))
                continue

            plugins.append(plugin)

        return plugins


# ----------------------------------------------------------------------
def _GetRepos(
    dm: DoneManager,
    session: _CustomSession,
    username: str,
    includes: list[str],
    excludes: list[str],
    *,
    ignore_archived: bool,
    ignore_forks: bool,
) -> list[str]:
    repositories: list[str] = []
    found = 0

    with dm.Nested(
        "Getting repositories...",
        [
            lambda: "{} found".format(inflect.no("repository", found)),
            lambda: "{} matched".format(inflect.no("repository", len(repositories))),
        ],
        suffix="\n",
    ) as repos_dm:
        include_exprs = _CreateRegexes(includes)
        exclude_exprs = _CreateRegexes(excludes)

        del includes
        del excludes

        page = 1
        per_page = 25

        while True:
            response = session.get(
                "{}/{}/repos".format(
                    "orgs" if session.is_enterprise else "users",
                    username,
                ),
                params={
                    "page": page,
                    "per_page": per_page,
                },
            )

            page += 1

            response.raise_for_status()

            try:
                response = response.json()
            except requests.exceptions.JSONDecodeError as ex:
                temp_filename = CurrentShell.CreateTempFilename(".html")

                with temp_filename.open("w") as f:
                    f.write(response.text)

                repos_dm.WriteError("The response content was not valid JSON; it has been saved at '{}' (Error: {}).\n".format(temp_filename, ex))
                return []

            if not response:
                break

            found += len(response)

            for response_item in response:
                repository = response_item["name"]

                if response_item["disabled"]:
                    repos_dm.WriteVerbose("'{}' is disabled.\n".format(repository))
                    continue

                if ignore_archived and response_item["archived"]:
                    repos_dm.WriteVerbose("'{}' is archived.\n".format(repository))
                    continue

                if ignore_forks and response_item["fork"]:
                    repos_dm.WriteVerbose("'{}' is a fork.\n".format(repository))
                    continue

                if exclude_exprs and any(expr.match(repository) for expr in exclude_exprs):
                    repos_dm.WriteVerbose("'{}' was excluded.\n".format(repository))
                    continue

                if include_exprs and not any(expr.match(repository) for expr in include_exprs):
                    repos_dm.WriteVerbose("'{}' was not included.\n".format(repository))
                    continue

                repositories.append(repository)

        return repositories


# ----------------------------------------------------------------------
def _ValidateRepo(
    dm: DoneManager,
    session: _CustomSession,
    username: str,
    repository: str,
    plugins: list[Plugin],
) -> None:
    grouped_plugins: dict[Plugin.ConfigurationType, list[Plugin]] = {}

    for plugin in plugins:
        grouped_plugins.setdefault(plugin.configuration_type, []).append(plugin)

    # ----------------------------------------------------------------------
    def RunPlugins(
        header: str,
        url: str,
        plugins: Optional[list[Plugin]],
    ) -> None:
        if plugins is None:
            return

        with dm.Nested(
            header,
            suffix="\n",
        ) as run_dm:
            response = session.get(url)

            response.raise_for_status()
            response = response.json()

            with run_dm.Nested("Running {}...".format(inflect.no("plugin", len(plugins)))) as plugin_dm:
                # ----------------------------------------------------------------------
                def EnumResults(
                    results: Plugin.ValidateResultType,
                ) -> Iterator[tuple[Plugin.MessageType, str]]:
                    if results is None:
                        return

                    if not isinstance(results, list):
                        results = [results, ]

                    for result in results:
                        if isinstance(result, str):
                            message_type = Plugin.MessageType.Error
                            message = result
                        else:
                            message_type, message = result

                        yield message_type, message

                # ----------------------------------------------------------------------

                for plugin in plugins:
                    try:
                        results = plugin.Validate(response)
                    except KeyError:
                        if session.has_pat:
                            raise

                        results = (
                            Plugin.MessageType.Warning,
                            "The configuration information used by this plugin was not found. This can generally be resolved by providing a GitHub Personal Access Token (PAT) on the command line.",
                        )

                    for message_type, message in EnumResults(results):
                        message = "[{}] {}".format(plugin.name, message)

                        if message_type == Plugin.MessageType.Error:
                            plugin_dm.WriteError(message)
                        elif message_type == Plugin.MessageType.Warning:
                            plugin_dm.WriteWarning(message)
                        elif message_type == Plugin.MessageType.Info:
                            plugin_dm.WriteInfo(message)
                        else:
                            assert False, message_type  # pragma: no cover

    # ----------------------------------------------------------------------

    RunPlugins(
        "Checking repository...",
        "repos/{}/{}".format(username, repository),
        grouped_plugins.get(Plugin.ConfigurationType.Repository),
    )

    RunPlugins(
        "Checking branches...",
        "repos/{}/{}/branches/main".format(username, repository),
        grouped_plugins.get(Plugin.ConfigurationType.Branch),
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
