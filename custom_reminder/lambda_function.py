from datetime import date, datetime
import os
import sys
import tempfile

from gspread import service_account

# AWS Lambdaでpost_slack Layerからもimportできるように設定
sys.path.append("/opt/slack_post_layer")
from postslack import post_slack  # NOQA


# 環境変数が設定されていないときはKeyErrorで落とす
SERVICE_ACCOUNT_CONTENTS = os.environ["SERVICE_ACCOUNT_CONTENTS"]
SPREAD_ID = os.environ["SPREAD_ID"]


def is_bigger_date(first, second):
    # firstかsecondのどちらかがdateでもう片方がdatetime
    if isinstance(first, datetime):
        first = date(first.year, first.month, first.day)
    if isinstance(second, datetime):
        second = date(second.year, second.month, second.day)
    return first < second


def lambda_handler(event, context):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]  # デフォルトのスコープ
    with tempfile.NamedTemporaryFile() as tempf:
        tempf.write(SERVICE_ACCOUNT_CONTENTS.encode())
        tempf.seek(0)
        gc = service_account(tempf.name, scopes)

    # カスタムリマインダー用のシート（サービスアカウントの追加が必要）
    spreadsheet = gc.open_by_key(SPREAD_ID)
    worksheet = spreadsheet.sheet1

    all_rows_list = worksheet.get_all_values()

    start_column = "start"
    end_column = "end"
    channel_column = "channel"
    text_column = "text"
    url_column = "url"

    header = all_rows_list[0]
    start_index = header.index(start_column)
    end_index = header.index(end_column)
    channel_index = header.index(channel_column)
    text_index = header.index(text_column)
    url_index = header.index(url_column)

    today = date.today()

    for row in all_rows_list[1:]:
        if is_bigger_date(
            today, datetime.strptime(row[start_index], "%Y/%m/%d")
        ) or is_bigger_date(
            datetime.strptime(row[end_index], "%Y/%m/%d"), today
        ):
            continue

        channel = row[channel_index]
        message = (
            f"{row[end_index]}まで繰り返すReminderです\n"
            f"{row[text_index]} {row[url_index]}"
        )
        post_slack(channel, message)


if __name__ == "__main__":
    lambda_handler(None, None)
