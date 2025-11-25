# SQS Queue Policy - CRITICAL: Allows S3 to send messages
resource "aws_sqs_queue_policy" "s3_to_sqs_policy" {
  queue_url = aws_sqs_queue.s3_event_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.s3_event_queue.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_s3_bucket.source_bucket.arn
          }
        }
      }
    ]
  })
}

resource "aws_sqs_queue" "s3_event_queue_dlq"{
  name                       = "s3_event_dlq"
  message_retention_seconds  = 1209600 # 14 days
  visibility_timeout_seconds = 30
  tags = {
    Environment = "production"
    Purpose     = "DLQ"
  }
}



resource "aws_sqs_queue" "s3_event_queue" {
  name = "s3-event-queue"
  message_retention_seconds  = 345600 # 4 days
  visibility_timeout_seconds = 30
  redrive_policy = jsonencode({
  deadLetterTargetArn = aws_sqs_queue.s3_event_queue_dlq.arn
  maxReceiveCount     = 1 # Number of times a message can be received before moving to DLQ
  })
}