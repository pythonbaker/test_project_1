output "sns_topic_arn" {
  value = "${aws_sns_topic.my_topic.arn}"
}

output "sns_subscription_arn" {
  value = "${aws_sns_topic_subscription.email.arn}"
}