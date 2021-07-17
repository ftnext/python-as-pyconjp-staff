from helium import S, click, find_all, kill_browser, press, scroll_down, write
from selenium.webdriver.common.keys import Keys


def find_element_by_id(id_value):
    # idなので1つの要素しか見つからない。それを返す
    return find_all(S(f"#{id_value}"))[0]


def input_connpass_form_item(element, value, is_adding_mode=False):
    click(element)  # カーソルが置かれ、フォーム（input要素）に切り替わる
    if not is_adding_mode:
        press(Keys.COMMAND + "a")  # MacOS前提で全選択（上書きするため）
    write(value)


def input_datetime(element, value, table_header):
    input_connpass_form_item(element, value)
    # elementをクリックしたときに開いている日付選択ウィジェットを閉じる
    click(table_header)


# タイトルの変更
field_title = find_element_by_id("FieldTitle")
input_connpass_form_item(field_title, "イベントタイトル")
click("保存")

# 時間の変更
starts = find_all(S(".start > td > span"))
# startsはイベント開始日の日・時、募集開始日の日・時の4要素からなる
click(starts[0])  # 開始日をクリック（時間全体が変更できるようになる）
start_inputs = find_all(S(".StartDate > td > input"))
input_datetime(start_inputs[0], "2021/07/16", "開始日時")
input_datetime(start_inputs[1], "20:30", "開始日時")

end_inputs = find_all(S(".EndDate > td > input"))
input_datetime(end_inputs[0], "2021/07/16", "終了日時")
input_datetime(end_inputs[1], "21:30", "終了日時")
click("保存")

scroll_down()  # 参加者への情報までスクロール
field_participant_only = find_element_by_id("FieldParticipantOnlyInfo")
input_connpass_form_item(
    field_participant_only, "\n\nhttps://example.com\n", is_adding_mode=True
)
click("保存")

kill_browser()
