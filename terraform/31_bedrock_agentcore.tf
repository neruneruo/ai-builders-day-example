###############################################################################
# Amazon Bedrock AgentCore                                                    #
###############################################################################
resource "aws_bedrockagentcore_agent_runtime" "example" {
  depends_on = [
    terraform_data.image_push,
  ]

  agent_runtime_name = local.bac_runtime_name
  role_arn           = aws_iam_role.example.arn

  agent_runtime_artifact {
    container_configuration {
      container_uri = "${aws_ecr_repository.example.repository_url}:latest"
    }
  }

  authorizer_configuration {
    custom_jwt_authorizer {
      discovery_url    = "https://${var.auth0_domain}/.well-known/openid-configuration"
      allowed_audience = [auth0_resource_server.example.identifier]
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  request_header_configuration {
    request_header_allowlist = [
      "Authorization",
    ]
  }

  environment_variables = {
    AWS_REGION                      = data.aws_region.current.region
    AWS_DEFAULT_REGION              = data.aws_region.current.region
    AWS_BEDROCK_AGENTCORE_MEMORY_ID = aws_bedrockagentcore_memory.example.id
    STRANDS_LOG_LEVEL               = "WARNING"
    AGENT_LOG_LEVEL                 = "WARNING"
    AGENT_STREAM_MODE               = "true"
  }
}

###############################################################################
# Amazon Bedrock AgentCore Memory                                             #
###############################################################################
resource "aws_bedrockagentcore_memory" "example" {
  name                  = local.bac_memory_name
  description           = "Example Memory"
  event_expiry_duration = 7
}
