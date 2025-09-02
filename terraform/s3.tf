resource "aws_s3_bucket" "test_bucket" {
  bucket = "test-bucket-s3-80469"

  tags = {
    Name        = "Test"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "test_bucket" {
  bucket = aws_s3_bucket.test_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "lambda_access" {
  bucket = aws_s3_bucket.test_bucket.id
  policy = data.aws_iam_policy_document.lambda_access.json
}

data "aws_iam_policy_document" "lambda_access" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.test_lambda.arn]
    }

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.test_bucket.arn,
      "${aws_s3_bucket.test_bucket.arn}/*",
    ]
  }
}
