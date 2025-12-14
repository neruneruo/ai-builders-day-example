###############################################################################
# Auth0 Client (Amazon Bedrock AgentCore Runtime authorization)               #
###############################################################################
resource "auth0_client" "example" {
  name        = "AI Builders Day Example Application"
  description = "Example Application for AI Builders Day"
  app_type    = "regular_web"

  custom_login_page_on                = false
  is_first_party                      = true
  is_token_endpoint_ip_header_trusted = false
  oidc_conformant                     = true
  require_proof_of_possession         = false

  grant_types = [
    "authorization_code",
    "refresh_token",
  ]

  callbacks = [
    "http://localhost:8501/",
  ]

  allowed_logout_urls = [
    "http://localhost:8501/",
  ]

  jwt_configuration {
    alg                 = "RS256"
    lifetime_in_seconds = 3600
    secret_encoded      = false
  }

  refresh_token {
    leeway          = 0
    token_lifetime  = 31557600
    rotation_type   = "non-rotating"
    expiration_type = "non-expiring"
  }
}

resource "auth0_client_credentials" "example" {
  client_id = auth0_client.example.client_id
}

resource "auth0_resource_server" "example" {
  name        = "AI Builders Day Example Resource Server"
  identifier  = "urn:${local.auth0_resource_server_id}:api"
  signing_alg = "RS256"

  allow_offline_access                            = false
  token_lifetime                                  = 7200
  skip_consent_for_verifiable_first_party_clients = false
  enforce_policies                                = true
  token_dialect                                   = "access_token"
}

resource "auth0_resource_server_scope" "example" {
  resource_server_identifier = auth0_resource_server.example.identifier

  scope       = "invoke:agent"
  description = "AIエージェントの実行"
}

resource "auth0_role" "example" {
  name = "AgentInvokeRole"
}

resource "auth0_role_permissions" "example" {
  role_id = auth0_role.example.id

  permissions {
    resource_server_identifier = auth0_resource_server.example.identifier
    name                       = auth0_resource_server_scope.example.scope
  }
}

###############################################################################
# Auth0 User                                                                  #
###############################################################################
resource "auth0_user" "example" {
  password       = "ai-builders-day-guest1234"
  email          = "ai-builders-day-guest@nec.com"
  email_verified = true

  connection_name = "Username-Password-Authentication"
}

resource "auth0_user_roles" "example" {
  user_id = auth0_user.example.id

  roles = [
    auth0_role.example.id
  ]
}