################################################################################
# IAM                                                                          #
################################################################################
resource "aws_iam_role" "example" {
  name               = local.iam_role_name
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

data "aws_iam_policy_document" "assume" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "bedrock-agentcore.amazonaws.com",
      ]
    }

    actions = [
      "sts:AssumeRole",
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values = [
        data.aws_caller_identity.self.id,
      ]
    }

    condition {
      test     = "ArnLike"
      variable = "AWS:SourceArn"
      values = [
        "arn:aws:bedrock-agentcore:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:*",
      ]
    }
  }
}

resource "aws_iam_role_policy" "custom" {
  name   = local.iam_policy_name
  role   = aws_iam_role.example.id
  policy = data.aws_iam_policy_document.custom.json
}

data "aws_iam_policy_document" "custom" {
  statement {
    effect = "Allow"

    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    ]

    resources = [
      "arn:aws:ecr:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:repository/*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "logs:DescribeLogStreams",
      "logs:CreateLogGroup",
    ]

    resources = [
      "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:log-group:/aws/bedrock-agentcore/runtimes/*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "logs:DescribeLogGroups",
    ]

    resources = [
      "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:log-group:*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords",
      "xray:GetSamplingRules",
      "xray:GetSamplingTargets",
    ]

    resources = [
      "*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "cloudwatch:PutMetricData",
    ]

    resources = [
      "*",
    ]

    condition {
      test     = "StringEquals"
      variable = "cloudwatch:namespace"
      values = [
        "bedrock-agentcore",
      ]
    }
  }
  statement {
    effect = "Allow"

    actions = [
      "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
    ]

    resources = [
      "arn:aws:bedrock-agentcore:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:workload-identity-directory/default",
      "arn:aws:bedrock-agentcore:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:workload-identity-directory/default/workload-identity/*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream",
    ]

    resources = [
      "arn:aws:bedrock:*::foundation-model/*",
      "arn:aws:bedrock:${data.aws_region.current.region}:${data.aws_caller_identity.self.id}:*",
      "arn:aws:bedrock:ap-northeast-1:${data.aws_caller_identity.self.id}:*",
    ]
  }
  statement {
    effect = "Allow"

    actions = [
      "bedrock-agentcore:CreateEvent",
      "bedrock-agentcore:ListEvents",
      "bedrock-agentcore:ListMemoryRecords",
    ]

    resources = [
      aws_bedrockagentcore_memory.example.arn,
    ]
  }
}
