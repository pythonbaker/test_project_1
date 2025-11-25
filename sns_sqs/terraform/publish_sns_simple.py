#!/usr/bin/env python3
"""
Simple SNS message publishing example
"""
import boto3
import json
from datetime import datetime


def publish_simple_message():
    """Publish a simple text message to SNS"""

    # Initialize SNS client
    sns_client = boto3.client("sns", region_name="us-east-1")

    # Your SNS topic ARN (replace with your actual ARN)
    topic_arn = "arn:aws:sns:us-east-1:954976299467:sonali-topic"

    # Simple message
    message = f"Hello from SNS! Sent at {datetime.now().isoformat()}"

    try:
        response = sns_client.publish(
            TopicArn=topic_arn, Message=message, Subject="Test Message from Python"
        )

        print(f"Message published successfully!")
        print(f"Message ID: {response['MessageId']}")
        return response["MessageId"]

    except Exception as e:
        print(f"Error publishing message: {str(e)}")
        return None


def publish_json_message():
    """Publish a structured JSON message to SNS"""

    sns_client = boto3.client("sns", region_name="us-east-1")
    topic_arn = "arn:aws:sns:us-east-1:954976299467:sonali-topic"

    # Structured data
    message_data = {
        "event_type": "user_signup",
        "user_id": "user_12345",
        "email": "user@example.com",
        "timestamp": datetime.now().isoformat(),
        "metadata": {"source": "web_app", "campaign": "summer_2025"},
    }

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message_data, indent=2),
            Subject="User Signup Event",
            MessageAttributes={
                "event_type": {"DataType": "String", "StringValue": "user_signup"},
                "priority": {"DataType": "String", "StringValue": "high"},
            },
        )

        print(f"JSON message published successfully!")
        print(f"Message ID: {response['MessageId']}")
        return response["MessageId"]

    except Exception as e:
        print(f"Error publishing JSON message: {str(e)}")
        return None


if __name__ == "__main__":
    print("Publishing simple message...")
    publish_simple_message()

    print("\nPublishing JSON message...")
    publish_json_message()
