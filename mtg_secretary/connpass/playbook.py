import os

from helium import (
    Text,
    click,
    start_firefox,
    wait_until,
    write,
)


def login():
    start_firefox("connpass.com/login")
    write(os.getenv("CONNPASS_USERNAME"), into="ユーザー名")
    write(os.getenv("CONNPASS_PASSWORD"), into="パスワード")
    click("ログインする")
    wait_until(Text("イベント管理").exists)
