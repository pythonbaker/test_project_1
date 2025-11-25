
resource "aws_iam_role" "sqs_lambda_role" {
 name= "lambda-execution-role"
 assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_s3_sqs_policy" {
    name ="lambda_s3_sqs_policy"
    role= aws_iam_role.sqs_lambda_role.name
    policy= jsonencode({
        Version = "2012-10-17"
    Statement = [
      # SQS Permissions
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl"
        ]
        Resource = [
          aws_sqs_queue.s3_event_queue.arn
        ]
      },
      # read s3 bucket
      {
         Effect = "Allow"
        Action = [
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:GetObjectMetadata",
             "s3:ListBucket"
        ]
        Resource =[
            "${aws_s3_bucket.source_bucket.arn}/*"
        ]
      },
      # destination s3 bucket write access
      {
        Effect = "Allow"
        Action= [
             "s3:PutObject",
             "s3:PutObjectAcl",
             "s3:ListBucket"
        ]
        Resource =[
            "${aws_s3_bucket.destination_bucket.arn}/*"
        ]
      },
      {
            Action = [
              "logs:CreateLogGroup",
              "logs:CreateLogStream",
              "logs:PutLogEvents",
            ]
            Effect   = "Allow"
            Resource = "arn:aws:logs:*:*:*"
          },

       ]
    })

}

# Create ZIP file for Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "lambda_triggered_by_sqs" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "sqs_trigger_lambda_function"
  role             = aws_iam_role.sqs_lambda_role.arn
  handler          = "lambda_function.handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime = "python3.11"
  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
    }
}
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.s3_event_queue.arn
  function_name    = aws_lambda_function.lambda_triggered_by_sqs.arn
  enabled          = true
  batch_size       = 5
}