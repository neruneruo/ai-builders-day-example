################################################################################
# Variables / Locals                                                           #
################################################################################
variable "prefix" {
  default = "ai-builders-day-example"
}

variable "default_tag_name" {
  type    = string
  default = "neruneruo"
}

variable "initial_apply" {
  type    = bool
  default = false
}

variable "auth0_domain" {
  type = string
}

variable "auth0_client_id" {
  type = string
}

variable "auth0_client_secret" {
  type = string
}

locals {
  ##############################################################################
  # Auth0                                                                      #
  ##############################################################################
  auth0_resource_server_id = "${var.prefix}-resource-server"

  ##############################################################################
  # IAM                                                                        #
  ##############################################################################
  iam_role_name   = "${var.prefix}-role"
  iam_policy_name = "${var.prefix}-policy"

  ##############################################################################
  # Amazon ECR                                                                 #
  ##############################################################################
  ecr_repository_name     = "${var.prefix}-repository"
  ecr_mcp_repository_name = "${var.prefix}-mcp_repository"

  ##############################################################################
  # Amazon Bedrock AgentCore                                                   #
  ##############################################################################
  bac_runtime_name = replace("${var.prefix}-runtime", "-", "_")
  bac_memory_name  = replace("${var.prefix}-memory", "-", "_")
}
