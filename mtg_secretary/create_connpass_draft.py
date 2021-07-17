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
    parser = argparse.ArgumentParser()
    common_options_parser = argparse.ArgumentParser(add_help=False)
    common_options_parser.add_argument("--kill_browser", action="store_true")
    subparsers = parser.add_subparsers(title="subcommand")

    login_parser = subparsers.add_parser(
        "login", parents=[common_options_parser]
    )
    login_parser.set_defaults(func=do_login)

    draft_parser = subparsers.add_parser(
        "draft", parents=[common_options_parser]
    )
    draft_parser.add_argument("event_info", type=Path)
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
