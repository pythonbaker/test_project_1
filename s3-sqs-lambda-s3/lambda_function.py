import json
import boto3
import os

# def handler(event, context):
#     print("This is the event record: ", event)
#     return {
#         'statusCode': 200,
#         'body': json.dumps({'message': 'Lambda is working!'})
#     }

#  extract the object key name and bucket name from the event data.
#  create s3 client to download the file and process them as per certain rules
# upload the file into the destination file.

s3 = boto3.client("s3")


def handler(event, context):
    print("this is the event record", json.dumps(event))
    try:
        bucket, key = extract_bucket(event)
        local_file = s3_file_download(bucket, key)
        print("the file has been downloaded")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "bucket": bucket,
                "key": key,
                "localFile": local_file
                }),
        }
    except Exception as e:
        print(f"Error handling event: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def extract_bucket(event):
    # extract s3 data from sqs event
    try:
        body = event["Records"][0]["body"]
        s3_event = json.loads(body)
        s3_record = s3_event["Records"][0]
        print("this is s3 record", json.dumps(s3_record))
        bucket = s3_record["s3"]["bucket"]["name"]
        key = s3_record["s3"]["object"]["key"]
        print(f"The bucket name is: {bucket} and object key: {key}")
    except Exception as e:
        raise ValueError(f"Invalid SQS/S3 event format: {e}")
    return bucket, key


def s3_file_download(bucket, key):

    # local_file = local_dummy_file.csv
    local_file = os.path.join("/tmp", os.path.basename(key))

    try:
        s3.download_file(bucket, key, local_file)
        print(f"File '{key}' downloaded to '{local_file}'")
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise RuntimeError(f"Could not download file from S3: {e}")
    return local_file
