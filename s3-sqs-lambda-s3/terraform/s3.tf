
resource "aws_s3_bucket" "source_bucket" {
  bucket = "source-bucket-80469"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.source_bucket.id

  queue {
    queue_arn = aws_sqs_queue.s3_event_queue.arn
    events    = ["s3:ObjectCreated:*"]
    # filter_suffix = ".log"  # Commented out to receive notifications for all files
  }
  depends_on = [aws_sqs_queue_policy.s3_to_sqs_policy]
}

resource "aws_s3_bucket" "destination_bucket" {
  bucket = "destination-bucket-80469"
}
