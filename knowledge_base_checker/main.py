import os
import sys

from atlassian import Confluence


def verify_environment_variables():
    return os.getenv("ATLASSIAN_EMAIL") and os.getenv("ATLASSIAN_API_TOKEN")


if __name__ == "__main__":
    if not verify_environment_variables():
        sys.exit(
            "Make sure that the environment variables ATLASSIAN_EMAIL and "
            "ATLASSIAN_API_TOKEN are set."
        )

    confluence = Confluence(
        url="https://pyconjp.atlassian.net",
        username=os.getenv("ATLASSIAN_EMAIL"),
        password=os.getenv("ATLASSIAN_API_TOKEN"),
    )
