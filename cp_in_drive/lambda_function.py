import json
import os
from urllib.request import Request, urlopen

import boto3
from operate_drive import create_diy_gdrive
from operate_drive.drive import DiyGoogleDrive
from operate_drive.file import DiyGDriveFile


REGION_NAME = os.environ["REGION_NAME"]
CLIENT_CONFIG_SECRET = os.environ["CLIENT_CONFIG_SECRET_NAME"]
SAVED_CREDENTIALS_SECRET = os.environ["SAVED_CREDENTIALS_SECRET_NAME"]


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


def fetch_secret_string(client, secret_id):
    secret_value_response = client.get_secret_value(SecretId=secret_id)
    return secret_value_response["SecretString"]


def lambda_handler(event, context):
    target_id = event["target_id"]
    response_url = event["response_url"]

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=REGION_NAME
    )
    client_config_string = fetch_secret_string(client, CLIENT_CONFIG_SECRET)
    saved_credentials_string = fetch_secret_string(
        client, SAVED_CREDENTIALS_SECRET
    )
    # Lambda関数から書き込めるディレクトリ/tmp以下にファイルを作成（credentialのrefreshも発生する）
    with open("/tmp/my_client_secrets.json", "w") as clientf, open(
        "/tmp/saved_credentials.json", "w"
    ) as credf:
        clientf.write(client_config_string)
        clientf.seek(0)
        credf.write(saved_credentials_string)
        credf.seek(0)

        copied_file = cp_in_drive(target_id)

    access_url = copied_file.fetch_url()

    message = {"text": f"Copied!\n{access_url}"}
    body = json.dumps(message).encode()
    request = Request(response_url, data=body)
    with urlopen(request) as res:
        return res.getcode()
