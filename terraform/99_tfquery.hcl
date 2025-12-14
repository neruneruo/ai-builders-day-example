list "aws_cloudwatch_log_group" "example" {
  provider = aws

  config {
    filter {
      name   = "tag:Name"
      values = ["instance-b", "instance-c"]
    }
  }
}