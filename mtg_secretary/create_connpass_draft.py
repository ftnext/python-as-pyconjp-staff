import argparse

from helium import kill_browser

from connpass.playbook import login


def do_login(args):
    login()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kill_browser", action="store_true")
    subparsers = parser.add_subparsers(title="subcommand")

    login_parser = subparsers.add_parser("login")
    login_parser.set_defaults(func=do_login)

    args = parser.parse_args()

    args.func(args)

    if args.kill_browser:
        kill_browser()
    else:
        while True:
            if input("qで終了: ") == "q":
                kill_browser()
                break
