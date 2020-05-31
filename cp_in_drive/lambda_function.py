from datetime import datetime
import hashlib
import hmac
import os
import shutil
from urllib import parse

from operate_drive import create_diy_gdrive
from operate_drive.drive import DiyGoogleDrive
from operate_drive.file import DiyGDriveFile


SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")


def is_verified(headers, body):
    signature = headers["X-Slack-Signature"]
    request_ts = int(headers["X-Slack-Request-Timestamp"])
    now_ts = int(datetime.now().timestamp())
    message = f"v0:{request_ts}:{body}"
    hmac_obj = hmac.new(
        bytes(SIGNING_SECRET, "UTF-8"), bytes(message, "UTF-8"), hashlib.sha256
    )
    expected = f"v0={hmac_obj.hexdigest()}"

    if abs(request_ts - now_ts) > (60 * 5) or not hmac.compare_digest(
        expected, signature
    ):
        return False
    return True


def cp_in_drive(source_id: str) -> DiyGDriveFile:
    """Copy a specified file in Google Drive and return the created file."""
    drive = create_diy_gdrive()
    dest_title = build_dest_title(drive, source_id)
    return drive.copy_file(source_id, dest_title)


def build_dest_title(drive: DiyGoogleDrive, source_id: str) -> str:
    source = drive.fetch_file_by_id(source_id)
    source_title = source.fetch_title()
    return title_of_copy_dest(source_title)


def title_of_copy_dest(source_title: str) -> str:
    # 暫定的に、元のファイル名にcopied_をつけるものとする
    return f"copied_{source_title}"


def lambda_handler(event, context):
    if not is_verified(event["headers"], event["body"]):
        return {"text": "Something went wrong..."}
    target_id = parse.parse_qs(event["body"])["text"][0]

    # credentialをrefreshするため、書き込めるディレクトリ/tmp以下にコピーを作成
    saved_secret_file = "saved_credentials.json"
    saved_secret_tmp_path = "/tmp/" + saved_secret_file
    shutil.copy2(saved_secret_file, saved_secret_tmp_path)

    # TODO: 呼び出してから3秒で終了しないため、Slackではエラー表示。しかしコピーはできる
    cp_in_drive(target_id)
    return {"text": "Copying now..."}
