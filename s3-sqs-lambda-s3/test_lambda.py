#!/usr/bin/env python3
"""
Test script for Lambda function with realistic S3-SQS event
"""
import json
import sys
import os

# Add current directory to path so we can import lambda_function
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import handler

def test_lambda_with_real_event():
    """Test with realistic S3-SQS event"""
    
    # Realistic S3 event wrapped in SQS message
    test_event = {
        "Records": [
            {
                "messageId": "test-message-id-12345",
                "receiptHandle": "test-receipt-handle",
                "body": json.dumps({
                    "Records": [
                        {
                            "eventVersion": "2.1",
                            "eventSource": "aws:s3",
                            "awsRegion": "ap-southeast-2",
                            "eventTime": "2025-10-23T10:30:00.000Z",
                            "eventName": "ObjectCreated:Put",
                            "userIdentity": {
                                "principalId": "EXAMPLE"
                            },
                            "requestParameters": {
                                "sourceIPAddress": "127.0.0.1"
                            },
                            "responseElements": {
                                "x-amz-request-id": "EXAMPLE123456789",
                                "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                            },
                            "s3": {
                                "s3SchemaVersion": "1.0",
                                "configurationId": "testConfigRule",
                                "bucket": {
                                    "name": "source-bucket-80469",
                                    "ownerIdentity": {
                                        "principalId": "EXAMPLE"
                                    },
                                    "arn": "arn:aws:s3:::source-bucket-80469"
                                },
                                "object": {
                                    "key": "dummy_file1.csv",
                                    "size": 1024,
                                    "eTag": "0123456789abcdef0123456789abcdef",
                                    "sequencer": "0A1B2C3D4E5F678901"
                                }
                            }
                        }
                    ]
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1698060600000",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1698060600000"
                },
                "messageAttributes": {},
                "md5OfBody": "test-md5-hash",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:ap-southeast-2:954976299467:s3-event-queue",
                "awsRegion": "ap-southeast-2"
            }
        ]
    }
    
    print("🧪 Testing Lambda function with realistic S3-SQS event...")
    print("=" * 60)
    
    try:
        # Call the handler
        response = handler(test_event, None)
        
        print("✅ Lambda function executed successfully!")
        print(f"Response: {json.dumps(response, indent=2)}")
        
    except Exception as e:
        print(f"❌ Lambda function failed: {e}")
        import traceback
        traceback.print_exc()

def test_lambda_with_invalid_event():
    """Test with invalid event to check error handling"""
    
    print("\n🧪 Testing Lambda function with invalid event...")
    print("=" * 60)
    
    invalid_event = {
        "Records": [
            {
                "body": "invalid json"
            }
        ]
    }
    
    try:
        response = handler(invalid_event, None)
        print("✅ Error handling worked!")
        print(f"Response: {json.dumps(response, indent=2)}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_lambda_missing_records():
    """Test with missing Records"""
    
    print("\n🧪 Testing Lambda function with missing Records...")
    print("=" * 60)
    
    empty_event = {}
    
    try:
        response = handler(empty_event, None)
        print("✅ Error handling worked!")
        print(f"Response: {json.dumps(response, indent=2)}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("Lambda Function Test Suite")
    print("=" * 60)
    
    # Test 1: Valid event
    test_lambda_with_real_event()
    
    # Test 2: Invalid JSON in body
    test_lambda_with_invalid_event()
    
    # Test 3: Missing Records
    test_lambda_missing_records()
    
    print("\n" + "=" * 60)
    print("All tests completed!")