import os
import sys

from atlassian import Confluence
from bs4 import BeautifulSoup


def verify_environment_variables():
    return os.getenv("ATLASSIAN_EMAIL") and os.getenv("ATLASSIAN_API_TOKEN")


def trim_html_tags(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()


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

    space_content = confluence.get_space_content("pyconjp")
    pages = space_content["page"]["results"]
    print(f"{len(pages)} pages")
    print("-" * 40)

    for page in pages:
        title = page["title"]
        html_body = page["body"]["storage"]["value"]
        content = trim_html_tags(html_body)
        print(f"{title} ({len(content)} characters)")
