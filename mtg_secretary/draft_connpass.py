import argparse
from pathlib import Path

from helium import kill_browser

from connpass.data import EventInfo
from connpass.playbook import copy_template_event, draft_event, login


def do_login(args):
    login()


def do_draft(args):
    event_info = EventInfo.from_json(args.event_info)
    login()
    copy_template_event()
    draft_event(**event_info.as_dict())


if __name__ == "__main__":
    description = "Connpass event drafter by browser automation."
    parser = argparse.ArgumentParser(description=description)
    common_options_parser = argparse.ArgumentParser(add_help=False)
    common_options_parser.add_argument(
        "--kill_browser",
        action="store_true",
        help=(
            "Specify if you want to close browser window after operation "
            "(default: not specified, which means keeping the window open)."
        ),
    )
    subparsers = parser.add_subparsers(title="subcommand")

    login_parser = subparsers.add_parser(
        "login",
        parents=[common_options_parser],
        description="Log in to connpass.",
    )
    login_parser.set_defaults(func=do_login)

    draft_parser = subparsers.add_parser(
        "draft",
        parents=[common_options_parser],
        description="Draft connpass event with template after login.",
    )
    draft_parser.add_argument(
        "event_info",
        type=Path,
        help=(
            "Specify JSON file with represents event information "
            "(See example)."
        ),
    )
    draft_parser.set_defaults(func=do_draft)

    args = parser.parse_args()

    args.func(args)

    if args.kill_browser:
        kill_browser()
    else:
        while True:
            if input("qで終了: ") == "q":
                kill_browser()
                break
