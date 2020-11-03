import os
from argparse import ArgumentParser

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


def authorize_client():
    options = {"server": "https://pyconjp.atlassian.net"}
    email, api_token = os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")
    return JIRA(options, basic_auth=(email, api_token))


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


def list_epics(args):
    jira = authorize_client()
    epics_under_components = fetch_epics_by_component(jira, args.component)
    print_epics_as_bullet_line(epics_under_components)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("component", choices=COMPONENTS_2020)
    subparsers = parser.add_subparsers(title="mode")

    list_epics_parser = subparsers.add_parser("list_epics")
    list_epics_parser.set_defaults(func=list_epics)

    args = parser.parse_args()
    args.func(args)
