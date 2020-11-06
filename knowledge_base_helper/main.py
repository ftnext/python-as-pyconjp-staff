import os
import sys
from argparse import ArgumentParser
from collections import defaultdict

from jira import JIRA

COMPONENTS_2020 = [
    "0.全体",
    "1.事務局",
    "2.コンテンツ",
    "3.会場",
    "4.システム",
    "5.デザイン",
    "6.NOC",
    "7.配信",
]


def verify_environment_variables():
    return os.getenv("JIRA_EMAIL") and os.getenv("JIRA_API_TOKEN")


def authorize_client():
    options = {"server": "https://pyconjp.atlassian.net"}
    email, api_token = os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")
    return JIRA(options, basic_auth=(email, api_token))


def fetch_issues_by_component(jira_client, component):
    jql = f"project=NEZ and component in ({args.component}) order by key asc"
    return jira_client.search_issues(jql, maxResults=False)


def fetch_epics_by_component(jira_client, component):
    jql = (
        f"project=NEZ and component in ({args.component}) and issuetype=Epic "
        "order by key asc"
    )
    return jira_client.search_issues(jql)


def print_epics_as_bullet_line(epics):
    for epic in epics:
        print(f"* {epic.fields.summary}")
        print(f"  * ref: {epic.permalink()}")


def print_epic_subissues_as_bullet_line(epics, epic_to_subissues_map):
    for epic in epics:
        epic_key = epic.key
        print(f"* {epic.fields.summary} ({epic_key})")
        for subissue in epic_to_subissues_map[epic_key]:
            print(f"  * {subissue.fields.summary} ({subissue.key})")


def list_epics(client, args):
    epics_under_components = fetch_epics_by_component(client, args.component)
    print_epics_as_bullet_line(epics_under_components)


def list_epic_subissues(client, args):
    epics_under_components = fetch_epics_by_component(client, args.component)
    key_to_epic_map = {epic.key: epic for epic in epics_under_components}

    issues_under_components = fetch_issues_by_component(client, args.component)
    epic_to_subissues_map = defaultdict(list)
    for issue in issues_under_components:
        # customfield_10008 includes a key of the parent issue
        parent_key = issue.fields.customfield_10008
        if parent_key in key_to_epic_map:  # if parent is epic
            epic_to_subissues_map[parent_key].append(issue)

    print_epic_subissues_as_bullet_line(
        key_to_epic_map.values(), epic_to_subissues_map
    )


if __name__ == "__main__":
    if not verify_environment_variables():
        sys.exit(
            "Make sure that the environment variables JIRA_EMAIL and "
            "JIRA_API_TOKEN are set."
        )

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="mode", help="Choose a mode.")
    parser.add_argument(
        "component", choices=COMPONENTS_2020, help="Specify a component."
    )

    list_epics_parser = subparsers.add_parser(
        "list_epics", help="List epic issues by the specified component."
    )
    list_epics_parser.set_defaults(func=list_epics)

    list_epic_subissues_parser = subparsers.add_parser(
        "list_epic_subissues",
        help=(
            "List the child issues of epic issues by the specified component."
        ),
    )
    list_epic_subissues_parser.set_defaults(func=list_epic_subissues)

    args = parser.parse_args()
    jira = authorize_client()
    args.func(jira, args)
