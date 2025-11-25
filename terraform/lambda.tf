
# Create a simple Python Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"
  source_file = "../src/lambda_function.py"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "test_lambda_function"
  role          = aws_iam_role.test_lambda.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.9"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  memory_size   = 512
  timeout       = 30
  architectures = ["arm64"]
}

resource "aws_iam_role" "test_lambda" {
  name = "test_lambda_role"

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

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.test_lambda.name
}

resource "aws_iam_policy" "lambda_s3_policy" {
  name        = "lambda_s3_access_policy"
  description = "Policy for Lambda to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.test_bucket.arn,
          "${aws_s3_bucket.test_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
  role       = aws_iam_role.test_lambda.name
}

