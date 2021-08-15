import os

from helium import (
    Alert,
    S,
    Text,
    click,
    find_all,
    go_to,
    scroll_down,
    start_firefox,
    wait_until,
    write,
)

from connpass.operations import (
    find_element_by_id,
    input_connpass_form_item,
    input_datetime,
)


def login():
    start_firefox("connpass.com/login")
    write(os.getenv("CONNPASS_USERNAME"), into="ユーザー名")
    write(os.getenv("CONNPASS_PASSWORD"), into="パスワード")
    click("ログインする")
    wait_until(Text("イベント管理").exists)


def copy_template_event():
    go_to("connpass.com/editmanage")
    copy_events = find_all(S(".copyEvent"))
    first_copy_event = copy_events[0]  # テンプレートは未来の日付のため一番上
    click(first_copy_event)
    Alert().accept()

    wait_until(Text("下書き中").exists)


def copy_existing_event(event_url: str):
    """管理者権限を持つイベントをコピーする"""
    go_to(event_url)
    click("コピーを作成")
    Alert().accept()

    wait_until(Text("下書き中").exists)


def draft_event(
    title: str,
    start_date: str,
    start_time: str,
    end_date: str,
    end_time: str,
    mtg_url: str,
):
    # タイトルの変更
    field_title = find_element_by_id("FieldTitle")
    input_connpass_form_item(field_title, title)
    click("保存")

    # 時間の変更
    starts = find_all(S(".start > td > span"))
    # startsはイベント開始日の日・時、募集開始日の日・時の4要素からなる
    click(starts[0])  # 開始日をクリック（時間全体が変更できるようになる）
    start_inputs = find_all(S(".StartDate > td > input"))
    input_datetime(start_inputs[0], start_date, "開始日時")
    input_datetime(start_inputs[1], start_time, "開始日時")

    end_inputs = find_all(S(".EndDate > td > input"))
    input_datetime(end_inputs[0], end_date, "終了日時")
    input_datetime(end_inputs[1], end_time, "終了日時")
    click("保存")

    scroll_down(400)  # 「参加者への情報」までスクロール（編集時に保存が見える状態）
    field_participant_only = find_element_by_id("FieldParticipantOnlyInfo")
    input_connpass_form_item(
        field_participant_only, f"\n\n{mtg_url}\n", is_adding_mode=True
    )
    click("保存")
