from helium import S, click, find_all, press, write
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
