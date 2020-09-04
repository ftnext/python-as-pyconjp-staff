"""
Boilerplate lambda function for automation with Google Spreadsheet and Slack
"""

import os
import tempfile

from gspread import service_account
from postslack import post_slack


# 環境変数が設定されていないときはKeyErrorで落とす
SERVICE_ACCOUNT_CONTENTS = os.environ["SERVICE_ACCOUNT_CONTENTS"]
SPREAD_ID = os.environ["SPREAD_ID"]


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

    channel = "random"
    message = f"Test: シートの行数は{len(all_rows_list)}です"
    post_slack(channel, message)
