import boto3
import os

sns = boto3.client("sns")

def send_notification(message):

    sns.publish(
        TopicArn=os.environ["SNS_TOPIC_ARN"],
        Subject="File Processing",
        Message=message
    )
