import json
import shutil
from urllib.request import Request, urlopen

from operate_drive import create_diy_gdrive
from operate_drive.drive import DiyGoogleDrive
from operate_drive.file import DiyGDriveFile


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
    target_id = event["target_id"]
    response_url = event["response_url"]

    # credentialをrefreshするため、書き込めるディレクトリ/tmp以下にコピーを作成
    saved_secret_file = "saved_credentials.json"
    saved_secret_tmp_path = "/tmp/" + saved_secret_file
    shutil.copy2(saved_secret_file, saved_secret_tmp_path)

    copied_file = cp_in_drive(target_id)
    access_url = copied_file.fetch_url()

    message = {"text": f"Copied!\n{access_url}"}
    body = json.dumps(message).encode()
    request = Request(response_url, data=body)
    with urlopen(request) as res:
        return res.getcode()
