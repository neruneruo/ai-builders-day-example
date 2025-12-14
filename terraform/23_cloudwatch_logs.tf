################################################################################
# Amazon CloudWatch Logs                                                              #
################################################################################
locals {
  import_indicator = var.initial_apply ? {} : {
    "example" = "dummy"
  }
}

import {
  for_each = var.initial_apply ? {} : { "example" = "dummy" }

  to = aws_cloudwatch_log_group.bedrock_agentcore[0]
  id = "/aws/bedrock-agentcore/runtimes/${aws_bedrockagentcore_agent_runtime.example.agent_runtime_id}-DEFAULT"
}

resource "aws_cloudwatch_log_group" "bedrock_agentcore" {
  count = var.initial_apply ? 0 : 1

  name              = "/aws/bedrock-agentcore/runtimes/${aws_bedrockagentcore_agent_runtime.example.agent_runtime_id}-DEFAULT"
  retention_in_days = 3
}
