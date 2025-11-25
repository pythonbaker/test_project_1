output "sqs_arn" {
  value = aws_sqs_queue.s3_event_queue.arn
}
output "lambda_arn" {
  value = aws_sqs_queue.s3_event_queue.arn
}

