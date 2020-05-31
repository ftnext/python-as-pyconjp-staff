from datetime import datetime
import hashlib
import hmac
import os
from urllib import parse


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


def lambda_handler(event, context):
    if not is_verified(event["headers"], event["body"]):
        return {"text": "Something went wrong..."}
    text = parse.parse_qs(event["body"])["text"][0]
    return {"text": f"Hello {text}"}
