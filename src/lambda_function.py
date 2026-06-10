import json
import uuid
import boto3
import os

from validator import validate_csv
from processor import process_csv
from notifier import send_notification

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["AUDIT_TABLE"]
)

def lambda_handler(event, context):

    try:

        bucket = event["detail"]["bucket"]["name"]

        key = event["detail"]["object"]["key"]

        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        content = (
            response["Body"]
            .read()
            .decode("utf-8")
        )

        validate_csv(content)

        count = process_csv(content)

        file_id = str(uuid.uuid4())

        table.put_item(
            Item={
                "fileId": file_id,
                "fileName": key,
                "status": "SUCCESS",
                "recordCount": count
            }
        )

        send_notification(
            f"{key} processed. Records={count}"
        )

        return {
            "statusCode": 200
        }

    except Exception as e:

        table.put_item(
            Item={
                "fileId": str(uuid.uuid4()),
                "fileName": key,
                "status": "FAILED",
                "errorMessage": str(e)
            }
        )

        raise
