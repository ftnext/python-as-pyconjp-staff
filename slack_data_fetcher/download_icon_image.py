import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("slack_user_id", nargs="+")
    parser.add_argument("--output_root", "-O", type=Path)
    args = parser.parse_args()

    args.output_root.mkdir(exist_ok=True, parents=True)

    token = os.environ["SLACK_BOT_USER_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    user_info_url = "https://slack.com/api/users.info"
    for user_id in args.slack_user_id:
        user_info_args = {"user": user_id}
        user_info_req = Request(
            f"{user_info_url}?{urlencode(user_info_args)}",
            headers=headers,
            method="GET",
        )
        with urlopen(user_info_req) as res:
            response = json.loads(res.read())
        user_info = response["user"]
        image_url = user_info["profile"]["image_512"]

        user_name = (
            user_info["profile"]["display_name"] or user_info["real_name"]
        )
        with urlopen(image_url) as res, open(
            args.output_root / f"{user_name}.jpg", "wb"
        ) as fb:
            fb.write(res.read())
