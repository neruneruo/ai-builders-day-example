################################################################################
# Provider                                                                     #
################################################################################
locals {
  tags = {
    Name = var.default_tag_name
  }
}

provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = local.tags
  }
}

###############################################################################
# Auth0                                                                       #
###############################################################################
terraform {
  required_version = "~> 1.14.0"

  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.32.0"
    }
  }
}

provider "auth0" {
  domain        = var.auth0_domain
  client_id     = var.auth0_client_id
  client_secret = var.auth0_client_secret
}
