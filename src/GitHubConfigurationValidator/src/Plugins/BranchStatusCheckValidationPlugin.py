# ----------------------------------------------------------------------
# |
# |  BranchStatusCheckValidationPlugin.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-15 10:53:59
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

from datetime import datetime
from dateutil import parser as datetime_parser
from typing import Any, Callable, Iterator, Optional

import typer

from semantic_version import Version as SemVer

from Common_Foundation.Streams.DoneManager import DoneManager
from Common_Foundation.Types import overridemethod

from Common_FoundationEx.InflectEx import inflect
from Common_FoundationEx.TyperEx import TypeDefinitionsType

from GitHubConfigurationValidatorLib.GitHubSession import GitHubSession
from GitHubConfigurationValidatorLib.Plugin import Plugin as PluginBase


# ----------------------------------------------------------------------
class Plugin(PluginBase):
    # ----------------------------------------------------------------------
    @classmethod
    @overridemethod
    def GetInstantiationParameters(cls) -> TypeDefinitionsType:
        return {
            "no_branch_status_check_validation": (
                bool,
                typer.Option(
                    False,
                    "--no-branch-status-check-validation",
                    help="Disable branch status check validation.",
                ),
            ),
        }

    # ----------------------------------------------------------------------
    def __init__(
        self,
        no_branch_status_check_validation: bool,
    ):
        super(Plugin, self).__init__(
            "BranchStatusCheckValidation",
            PluginBase.ConfigurationType.Custom,
            SemVer("0.4.0"),
            "Validates that all actions executed on pull requests to the main branch are required.",
            textwrap.dedent(
                """\
                The jobs required during branch validation for a pull request should match the jobs
                that are executed during the pull request (otherwise, why are they run?).

                Identify the GitHub Jobs Executed
                ---------------------------------
                1) Visit '{{repository}}/actions'
                2) Select the GitHub workflow associated with pull requests
                3) Select the most recent run for that workflow
                4) Note the jobs executed during that workflow; this information will be used in the steps that follow.

                Ensure that Those Jobs are Required
                -----------------------------------
                5) Visit '{{repository}}'/settings/branches'
                6) Edit the branch protection rules for the default branch
                7) Locate the 'Require status checks to pass before merging' -> 'Status checks that are required.' section
                8) Search for the jobs identified in step 4, adding each that is not already listed.
                """,
            ),
            textwrap.dedent(
                """\
                All Job executed during a pull request should be required by the branch protection rules (otherwise
                why are the being run during a pull request?).

                Reasons for this Default
                ------------------------
                - Jobs run during a pull request provide information relevant to the overall Quality of
                  the pull request itself and should complete successfully for valid pull requests.

                Reasons to Override this Default
                --------------------------------
                - Jobs run during pull requests are not stable.
                """,
            ),
        )

        self._no_branch_status_check_validation         = no_branch_status_check_validation

    # ----------------------------------------------------------------------
    @overridemethod
    def Validate(
        self,
        configuration: dict[str, Any],  # pylint: disable=unused-argument
    ) -> PluginBase.ValidateResultType:
        raise Exception("This should never be called")

    # ----------------------------------------------------------------------
    @overridemethod
    def CustomValidate(
        self,
        dm: DoneManager,
        session: GitHubSession,
        repository: str,
    ) -> PluginBase.ValidateResultType:
        if self._no_branch_status_check_validation:
            return None

        # Get the default branch
        default_branch: Optional[str] = None

        with dm.Nested("Calculating default branch name...", lambda: "'{}'".format(default_branch)):
            response = session.get("repos/{}/{}".format(session.github_username, repository))

            response.raise_for_status()
            default_branch = response.json()["default_branch"]

        if default_branch is None:
            return "The default branch was not found."

        # Find the protection list
        protection_jobs: set[str] = set()

        with dm.Nested(
            "Calculating protection list for '{}'...",
            lambda: "{} found".format(inflect.no("branch protection job", len(protection_jobs))),
        ) as protection_dm:
            response = session.get("repos/{}/{}/branches/{}/protection".format(session.github_username, repository, default_branch))

            if response.status_code != 200:
                protection_dm.result = 1
                return (PluginBase.MessageType.Warning, "The '{}' branch is not protected (Code: {}).".format(default_branch, response.status_code))

            response = response.json()

            status_checks = response.get("required_status_checks", None)
            if status_checks is None:
                protection_dm.result = 1
                return (PluginBase.MessageType.Warning, "The '{}' branch is not protected (missing data).".format(default_branch))

            for check in status_checks["checks"]:
                protection_jobs.add(check["context"])

        # Find a matching pull request against that branch
        reference_sha: Optional[str] = None

        with dm.Nested("Searching for a pull request event against '{}'...".format(default_branch)) as pr_dm:
            for event in _EnumItems(
                session,
                "repos/{}/{}/pulls?state=all".format(session.github_username, repository),
            ):
                if event["base"]["ref"] == default_branch:
                    reference_sha = event["head"]["sha"]
                    break

            if reference_sha is None:
                pr_dm.result = 1
                return (PluginBase.MessageType.Warning, "No pull requests have been merged into '{}'.".format(default_branch))

        # Find a workflow run that corresponds to the commit associated with the pull request event
        reference_runs: list[dict[str, Any]] = []
        created_at: Optional[datetime] = None

        with dm.Nested("Searching for workflow runs associated with the pull request event...") as workflow_pr:
            for workflow in _EnumItems(
                session,
                "repos/{}/{}/actions/workflows".format(session.github_username, repository),
                lambda response: response["workflows"],
            ):
                for workflow_run in _EnumItems(
                    session,
                    "repos/{}/{}/actions/workflows/{}/runs".format(
                        session.github_username,
                        repository,
                        workflow["id"],
                    ),
                    lambda response: response["workflow_runs"],
                ):
                    this_date = datetime_parser.parse(workflow_run["created_at"])

                    if created_at is not None and this_date < created_at:
                        break

                    if workflow_run["head_sha"] == reference_sha:
                        reference_runs.append(workflow_run)
                        created_at = this_date
                        break

            if not reference_runs:
                workflow_pr.result = 1
                return (PluginBase.MessageType.Warning, "No workflow runs have been executed against the most recent pull request.")

        run_jobs: set[str] = set()

        with dm.Nested(
            "Extracting executed jobs...",
            lambda: "{} found".format(inflect.no("job", len(run_jobs))),
        ):
            for reference_run in reference_runs:
                for job in _EnumItems(
                    session,
                    "repos/{}/{}/actions/runs/{}/jobs".format(session.github_username, repository, reference_run["id"]),
                    lambda response: response["jobs"],
                ):
                    run_jobs.add(job["name"])

        if run_jobs.difference(protection_jobs):
            dm.WriteError(
                textwrap.dedent(
                    """\
                    Jobs Run
                    --------
                    {}

                    Jobs Required
                    -------------
                    {}
                    """,
                ).format(
                    "\n".join("{}) {}".format(index + 1, job) for index, job in enumerate(sorted(run_jobs))),
                    "\n".join("{}) {}".format(index + 1, job) for index, job in enumerate(sorted(protection_jobs))),
                ),
            )

            return "Differences were found between the jobs run and the jobs required by the branch protection rules."

        return None


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _EnumItems(
    session: GitHubSession,
    url: str,
    postprocess_response_func: Optional[Callable[[dict[str, Any]], dict[str, Any]]]=None,
) -> Iterator[dict[str, Any]]:
    page_index = 1
    page_size = 25

    url_template = "{}{}page={{page_index}}&per_page={}".format(
        url,
        "&" if "?" in url else "?",
        page_size,
    )

    while True:
        response = session.get(url_template.format(page_index=page_index))
        page_index += 1

        response.raise_for_status()
        response = response.json()

        if postprocess_response_func:
            response = postprocess_response_func(response)

        if not response:
            break

        yield from response  # type: ignore
