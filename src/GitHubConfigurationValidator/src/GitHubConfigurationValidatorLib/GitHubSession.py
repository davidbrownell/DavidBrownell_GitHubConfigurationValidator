# ----------------------------------------------------------------------
# |
# |  GitHubSession.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2023-11-15 10:27:10
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2023
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the GitHubSession object"""

from pathlib import Path
from typing import Optional

import requests


# ----------------------------------------------------------------------
class GitHubSession(requests.Session):
    """Session used to communicate with GitHub"""

    # ----------------------------------------------------------------------
    # |  Public Types
    DEFAULT_GITHUB_URL                      = "https://api.github.com"

    # ----------------------------------------------------------------------
    # |  Public Methods
    def __init__(
        self,
        github_url: str,
        github_username: str,
        github_pat: Optional[str],
        *args,
        **kwargs,
    ):
        super(GitHubSession, self).__init__(*args, **kwargs)

        if github_url.endswith("/"):
            github_url = github_url[:-1]

        self.headers.update(
            {
                "X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github+json",
            },
        )

        if github_pat:
            potential_file = Path(github_pat)

            if potential_file.is_file():
                with potential_file.open("r") as f:
                    github_pat = f.read().strip()

            self.headers["Authorization"] = "Bearer {}".format(github_pat)

        self.github_url                     = github_url
        self.github_username                = github_username
        self.is_enterprise                  = self.github_url != self.__class__.DEFAULT_GITHUB_URL
        self.has_pat                        = bool(github_pat)

    # ----------------------------------------------------------------------
    def request(
        self,
        method: str,
        url: str,
        *args,
        **kwargs,
    ):
        if not url.startswith("/"):
            url = "/{}".format(url)

        return super(GitHubSession, self).request(
            method,
            "{}{}".format(self.github_url, url),
            *args,
            **kwargs,
        )
