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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("component", choices=COMPONENTS_2020)
    args = parser.parse_args()

    options = {"server": "https://pyconjp.atlassian.net"}
    email, api_token = os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")
    jira = JIRA(options, basic_auth=(email, api_token))

    jql = (
        f"project=NEZ and component in ({args.component}) and issuetype=Epic "
        "order by key asc"
    )
    epics_under_components = jira.search_issues(jql)

    # エピックの一覧を箇条書きのマークアップとして出力する
    for epic in epics_under_components:
        print(f"* {epic.fields.summary}")
        print(f"  * ref: {epic.permalink()}")
