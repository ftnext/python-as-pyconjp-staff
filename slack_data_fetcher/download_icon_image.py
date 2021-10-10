import argparse
import json
import logging
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)

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
    users_count = len(args.slack_user_id)
    for i, user_id in enumerate(args.slack_user_id, start=1):
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
        if not image_url:
            # 2014年以前に設定されたアイコンには512サイズがないらしい
            image_url = user_info["profile"]["image_192"]

        user_name = (
            user_info["profile"]["display_name"] or user_info["real_name"]
        )
        with urlopen(image_url) as res, open(
            args.output_root / f"{user_name}.jpg", "wb"
        ) as fb:
            fb.write(res.read())

        logging.info("(%d/%d) %s: %s done", i, users_count, user_id, user_name)
