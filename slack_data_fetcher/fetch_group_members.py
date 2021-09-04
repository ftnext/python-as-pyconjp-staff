import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

if __name__ == "__main__":
    token = os.environ["SLACK_BOT_USER_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    groups_list_url = "https://slack.com/api/usergroups.list"
    groups_list_req = Request(groups_list_url, headers=headers, method="GET")
    with urlopen(groups_list_req) as res:
        response = json.loads(res.read())
    for group in response["usergroups"]:
        if group["handle"] == "2021-staff":
            staff_group_id = group["id"]
            break

    groups_users_list_url = "https://slack.com/api/usergroups.users.list"
    groups_users_list_args = {"usergroup": staff_group_id}
    groups_users_list_req = Request(
        f"{groups_users_list_url}?{urlencode(groups_users_list_args)}",
        headers=headers,
        method="GET",
    )
    with urlopen(groups_users_list_req) as res:
        response = json.loads(res.read())
    user_ids = response["users"]
    print(f"{len(user_ids)} members in {group['handle']}")

    user_info_url = "https://slack.com/api/users.info"
    users = []
    for user_id in user_ids:
        user_info_args = {"user": user_id}
        user_info_req = Request(
            f"{user_info_url}?{urlencode(user_info_args)}",
            headers=headers,
            method="GET",
        )
        with urlopen(user_info_req) as res:
            response = json.loads(res.read())
        user_info = response["user"]
        # 表示名が設定されていたらそれを使う。設定されていなければreal_nameを使う。
        # user_info["name"] は招待したメールアドレスのユーザ名が入る挙動らしい
        user_name = (
            user_info["profile"]["display_name"] or user_info["real_name"]
        )
        users.append({"name": user_name, "id": user_info["id"]})
    for user in sorted(users, key=lambda u: u["name"]):
        print(f"{user['name']}-{user['id']}")
