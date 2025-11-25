### This project is to practice when an file is uploaded in input s3 bucket, which sending an event to sqs queue
### which triggers the lambda, this lambda function
###  will process the csv file and upload into the destination bucket

```mermaid
flowchart TD
    A[S3 Bucket (Source)] -->|File Uploaded|
    B event -> [SQS Queue]
    B -->|Trigger| C[Lambda Function]
    C -->|Process & Copy File|
    D ->[S3 Bucket (Destination)]
```


Terraform for infrastructure:
- create source and destination s3 bucket,
- sqs that gets triggered when a file is uploaded in source s3
- and this sqs triggers lambda and moves file from source to destination s3 bucket

## AWS infrastructure
### S3 bucket
- Create input s3 bucket
-- which needs access to sqs queue to send message
-- an event created when a file is loaded and message sent to sqs queue
--Create an aws_s3_bucket_notification resource to link the S3 bucket to the SQS queue for specific events.

- Create destination s3 bucket

### SQS
- create a SQS queue
- create a role to allow sqs to send message once triggered from source bucket
- Create an aws_sqs_queue_policy resource to allow the S3 bucket to send messages to the SQS queue.
Add subscription to lambda

### Lambda
- Create a role ("aws_iam_role") for lambda to assume and then create a policy ("aws_iam_role_policy_attachment" ) which is linked to the role. The policy will allow access to get objects from source bucket and put objects to destination bucket and receive messages from sqs.
- create a lambda function ("aws_lambda_function") where role is attached to this function.
- create an aws_lambda_event_source_mapping to link SQS to lambda function to configure the trigger from SQS
- The lambda code is deployed as zip file, create "archive_file" data source to package the code into zip file. This filename is used in lambda function.


To apply the infra via cli
cd into s3-sqs-lambda-s3/terraform
- to validate terraform code - terraform validate
terraform init
terraform plan
terraform apply

### lambda code

Run the scripts to process the csv files
once done upload the file in destination SQS

Test:
# Disable SQS trigger for testing
aws lambda update-event-source-mapping --uuid YOUR_UUID --no-enabled

# Re-enable later
aws lambda update-event-source-mapping --uuid YOUR_UUID --enabled
aws lambda update-event-source-mapping --uuid b8a7ace9-c238-4a54-9641-0d6f233e49e3 --enabled

# Check status
aws lambda get-event-source-mapping --uuid YOUR_UUID
Touch the file in s3 bucket
aws s3 cp s3://source-bucket-80469/test.csv s3://source-bucket-80469/test.log
View the message in SQS
aws sqs receive-message --queue-url https://sqs.ap-southeast-2.amazonaws.com/954976299467/s3-event-queue

# Validate Code before deployment
-- flake8 (Static Analysis (logical/runtime errors like wrong arguments))
poetry add --group dev flake8
poetry run flake8 s3-sqs-lambda-s3/lambda_function.py
--Syntax errors (py_compile)
This only catches errors like missing : or unmatched parentheses:
-- test the lambda locally by using the event record
```python -c "from lambda_function import handler; handler({'Records':[{'body':'{\"Records\":[{\"s3\":{\"bucket\":{\"name\":\"source-bucket-80469\"},\"object\":{\"key\":\"dummy_file1.csv\"}}}]}'}]}, None)" ```

Test 1 :
Copy a dummy file to source bucket via aws cli:
```aws s3 cp /Users/sonali.cornelio/Downloads/dummy_file1.csv s3://source-bucket-80469/```
- check cloudwatch logs if it has triggered the lambda via sqs queue trigger.

Test2:
Deployed lambda code with syntax error, on uploading file in s3 lambda kept retrying many times. There was a syntax error in the code. The lambda code wasnt deployed, but sqs kept resending the messages.
Solution: to check syntax error, check the code before deploying (add a script)
```python -m py_compile ../lambda_function.py```
[Run python -m py_compile as part of your deployment script:
Use flake8 or pylint in your pipeline:
- pip install flake8
- flake8 lambda_function.py
Add to Terraform CI/CD pipeline:
- python -m py_compile src/lambda_function.py || exit 1]

-- set up dlq for sqs if it fails to stop retrying and add to dlq
You can configure a dead-letter queue (DLQ) and limit retries by using redrive_policy on the source SQS queue.