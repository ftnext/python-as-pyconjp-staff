import argparse
import json
import os
import random
import textwrap
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import jwt

from zoom.data import ScheduledMeetings

ZOOM_JWT_APP_API_KEY = os.environ["ZOOM_JWT_APP_API_KEY"]
ZOOM_JWT_APP_API_SECRET = os.environ["ZOOM_JWT_APP_API_SECRET"]


def issue_jwt_token():
    jwt_expiration = int(time.time()) + 5  # 5 seconds
    jwt_headers = {"alg": "HS256", "typ": "JWT"}
    jwt_payload = {"iss": ZOOM_JWT_APP_API_KEY, "exp": jwt_expiration}
    return jwt.encode(
        jwt_payload,
        ZOOM_JWT_APP_API_SECRET,
        algorithm="HS256",
        headers=jwt_headers,
    )


def do_request(endpoint, method, data=None):
    headers = {
        "authorization": f"Bearer {issue_jwt_token()}",
        "content-type": "application/json",
    }
    request = Request(endpoint, headers=headers, method=method)
    with urlopen(request, data=data) as res:
        return json.load(res)


def fetch_zoom_user_id():
    users_query = {"status": "active", "page_size": 10, "page_number": 1}
    users_endpoint = f"https://api.zoom.us/v2/users?{urlencode(users_query)}"
    users_result = do_request(users_endpoint, "GET")
    for user in users_result["users"]:
        if user["first_name"] == "PyCon":
            return user["id"]


def listup_meetings(args):
    user_id = fetch_zoom_user_id()
    meeting_list_query = {
        "type": "upcoming",
        "page_size": 10,
        "page_number": 1,
    }
    meeting_list_endpoint = (
        f"https://api.zoom.us/v2/users/{user_id}/meetings"
        f"?{urlencode(meeting_list_query)}"
    )
    meeting_result = do_request(meeting_list_endpoint, "GET")
    scheduled_meetings = ScheduledMeetings.from_json(
        meeting_result["meetings"]
    )
    for meeting in scheduled_meetings.sorted():
        print(meeting)
        print("-" * 40)


def create_random_passcode(length=7):
    charset = ["@", "-", "_", "*"]
    numbers = list("0123456789")
    lower_start = ord("a")
    lower_alphabet = [chr(lower_start + i) for i in range(26)]
    upper_start = ord("A")
    upper_alphabet = [chr(upper_start + i) for i in range(26)]
    charset.extend(numbers + lower_alphabet + upper_alphabet)
    random.shuffle(charset)
    return "".join(random.sample(charset, 1)[0] for _ in range(length))


def create_meeting(args):
    user_id = fetch_zoom_user_id()
    passcode = create_random_passcode()
    print(f"{passcode=}")

    meeting_creation_endpoint = (
        f"https://api.zoom.us/v2/users/{user_id}/meetings"
    )
    meeting_data = {
        "start_time": f"2021-{args.date}T{args.time}:00",
        "timezone": "Asia/Tokyo",
        "duration": 60 * args.duration,
        "topic": args.topic,
        # ref: https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/meetingcreate  # NOQA
        "type": 2,  # Scheduled meeting
        "password": passcode,
        "settings": {
            "join_before_host": True,
            "jbh_time": 0,  # join before the host anytime
            "waiting_room": False,
            "host_video": False,
            "participant_video": False,
            "mute_upon_entry": False,
            "auto_recording": "local",
        },
    }
    creation_result = do_request(
        meeting_creation_endpoint, "POST", json.dumps(meeting_data).encode()
    )
    print(creation_result["join_url"])


if __name__ == "__main__":
    description = "Zoom meeting scheduler."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(title="subcommand")

    list_parser_help = """\
    List up scheduled meetings.

    Example:
        python %(prog)s
    """
    list_parser = subparsers.add_parser(
        "list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(list_parser_help),
    )
    list_parser.set_defaults(func=listup_meetings)

    create_parser_help = """\
    Schedule a Zoom meeting.

    Example: Schedule 2 hours meeting from 2021-03-15 19:30.
        python %(prog)s 03-15 19:30 2 'Awesome meeting'
    """
    create_parser = subparsers.add_parser(
        "create",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(create_parser_help),
    )
    create_parser.add_argument(
        "date", help="Specify %%m-%%d format. (e.g. 03-09)"
    )
    create_parser.add_argument(
        "time", help="Specify %%H:%%M format. (e.g. 20:00)"
    )
    create_parser.add_argument("duration", type=int, help="Unit: hour.")
    create_parser.add_argument(
        "topic", help="Enclose by quotes when topic includes white spaces."
    )
    create_parser.set_defaults(func=create_meeting)

    args = parser.parse_args()

    args.func(args)
