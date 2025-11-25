#!/usr/bin/env python3
"""
A test to check how AWS Lambda Powertools S3Object works, it creates a txt file into the s3 bucket if not
present and  test_your_code_with_real_aws() function , reads the file using s3object from the s3 bucket and the text file
Using s3 object is more memory efficient.
Enter your S3 bucket name: test-s3-bucket-13
Enter your S3 object key: test-powertools-streaming.txt
"""

from aws_lambda_powertools.utilities.streaming import S3Object


def test_your_code_with_real_aws():
    """Test with real AWS (requires credentials and S3 access)"""
    print("\nTesting with real AWS...")

    # Get bucket and key from user
    bucket1 = input("Enter your S3 bucket name: ")
    print(bucket1)
    bucket = input("Enter your S3 bucket name: ").strip()
    print(bucket)
    key = input("Enter your S3 object key: ").strip()

    if not bucket or not key:
        print("Skipping real AWS test...")
        return

    try:
        # Using readlines() to read all lines at once. the output is [b'Hello from S3!\n', b'This is line 2\n', b'This is line 3'] which is in raw bytes format
        # Read all lines as bytes and decode each line to string
        s3_obj = S3Object(bucket=bucket, key=key)
        lines = s3_obj.readlines()  # returns a list of bytes
        decoded_lines = [line.decode("utf-8").rstrip("\n") for line in lines]
        print("Read lines:", decoded_lines)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure:")
        print("- AWS credentials are configured")
        print("- S3 bucket exists and you have read access")
        print("- S3 object exists")


def create_test_file():
    """Create a test file in S3 for testing"""
    import boto3

    bucket = input("Enter S3 bucket name to create test file: ").strip()
    if not bucket:
        return None, None

    try:
        s3 = boto3.client("s3")
        test_content = "Hello from S3!\nThis is line 2\nThis is line 3"
        key = "test-powertools-streaming.txt"

        s3.put_object(
            Bucket=bucket, Key=key, Body=test_content, ContentType="text/plain"
        )

        print(f"✅ Created test file: s3://{bucket}/{key}")
        return bucket, key

    except Exception as e:
        print(f"❌ Error creating test file: {e}")
        return None, None


if __name__ == "__main__":
    print("Testing AWS Lambda Powertools S3Object")
    print("=" * 50)


    # Ask if user wants to test with real AWS
    choice = input("\nTest with real AWS? (y/n): ").lower()
    if choice == "y":
        create_choice = input("Create test file first? (y/n): ").lower()

        if create_choice == "y":
            bucket, key = create_test_file()
            print(f"this is the {bucket},{key}")
            if bucket and key:
                print("\nNow testing with created file...")
                try:
                    line = S3Object(bucket=bucket, key=key).readline()
                    print(line)
                    print("✅ Test successful!")
                except Exception as e:
                    print(f"❌ Error: {e}")
        else:
            test_your_code_with_real_aws()

    print("\n" + "=" * 50)
    print("Test is complete")

