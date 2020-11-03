import os

from jira import JIRA

if __name__ == "__main__":
    options = {"server": "https://pyconjp.atlassian.net"}
    email, api_token = os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")
    jira = JIRA(options, basic_auth=(email, api_token))
