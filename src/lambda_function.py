import json
import uuid
import boto3
import os

from src.validator import validate_csv
from src.processor import process_csv
from src.notifier import send_notification

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["AUDIT_TABLE"]
)


def lambda_handler(event, context):

    bucket = None
    key = None

    try:

        # Support both S3 Trigger and EventBridge

        if "Records" in event:

            bucket = (
                event["Records"][0]
                ["s3"]["bucket"]["name"]
            )

            key = (
                event["Records"][0]
                ["s3"]["object"]["key"]
            )

        else:

            bucket = (
                event["detail"]["bucket"]["name"]
            )

            key = (
                event["detail"]["object"]["key"]
            )

        # Prevent recursive processing

        if not key.startswith("incoming/"):

            print(
                f"Ignoring file outside incoming folder: {key}"
            )

            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "message": "Ignored"
                    }
                )
            }

        print(
            f"Processing file: {key}"
        )

        # Read file from S3

        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        content = (
            response["Body"]
            .read()
            .decode("utf-8")
        )

        # Validate file

        validate_csv(content)

        # Process file

        count = process_csv(content)

        # Audit Success

        file_id = str(uuid.uuid4())

        table.put_item(
            Item={
                "fileId": file_id,
                "fileName": key,
                "status": "SUCCESS",
                "recordCount": count
            }
        )

        # Send Notification

        send_notification(
            f"{key} processed successfully. "
            f"Records={count}"
        )

        # Move file to processed folder

        file_name = key.split("/")[-1]

        s3.copy_object(
            Bucket=bucket,
            CopySource={
                "Bucket": bucket,
                "Key": key
            },
            Key=f"processed/{file_name}"
        )

        s3.delete_object(
            Bucket=bucket,
            Key=key
        )

        print(
            f"Moved file to processed/{file_name}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "File processed successfully",
                    "recordCount": count
                }
            )
        }

    except Exception as e:

        print(
            f"Error: {str(e)}"
        )

        # Audit Failure

        try:

            table.put_item(
                Item={
                    "fileId": str(uuid.uuid4()),
                    "fileName": (
                        key if key else "UNKNOWN"
                    ),
                    "status": "FAILED",
                    "errorMessage": str(e)
                }
            )

        except Exception as audit_error:

            print(
                f"Audit logging failed: "
                f"{str(audit_error)}"
            )

        # Move failed file

        try:

            if bucket and key:

                file_name = key.split("/")[-1]

                s3.copy_object(
                    Bucket=bucket,
                    CopySource={
                        "Bucket": bucket,
                        "Key": key
                    },
                    Key=f"failed/{file_name}"
                )

                s3.delete_object(
                    Bucket=bucket,
                    Key=key
                )

                print(
                    f"Moved file to failed/{file_name}"
                )

        except Exception as move_error:

            print(
                f"Failed moving file: "
                f"{str(move_error)}"
            )

        raise
