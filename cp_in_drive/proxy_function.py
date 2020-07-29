from datetime import datetime
import hashlib
import hmac
import json
import os
from urllib import parse

import boto3


SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
REGION_NAME = os.environ.get("REGION_NAME")
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")


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


def lambda_handler(event, context):
    if not is_verified(event["headers"], event["body"]):
        return {"text": "Something went wrong..."}

    target_id = parse.parse_qs(event["body"])["text"][0]
    response_url = parse.parse_qs(event["body"])["response_url"][0]
    payload = {"target_id": target_id, "response_url": response_url}

    step_function = boto3.client("stepfunctions", region_name=REGION_NAME)
    step_function.start_execution(
        stateMachineArn=STATE_MACHINE_ARN, input=json.dumps(payload)
    )
    return {"text": "Copying now..."}
