################################################################################
# Local file                                                                   #
################################################################################
resource "local_file" "agent_env_shell" {
  filename = "../agents/env.sh"
  content = templatefile("${path.module}/template_file/env.sh.tmpl", {
    aws_region          = data.aws_region.current.region
    agent_runtime_arn   = aws_bedrockagentcore_agent_runtime.example.agent_runtime_arn
    agentcore_memory_id = aws_bedrockagentcore_memory.example.id
  })
}

resource "local_file" "ui_dotenv" {
  filename = "../ui/src/ui/.env"
  content = templatefile("${path.module}/template_file/.env.tmpl", {
    aws_region        = data.aws_region.current.region
    agent_runtime_arn = aws_bedrockagentcore_agent_runtime.example.agent_runtime_arn
  })
}

resource "local_file" "ui_streamlit_secrets" {
  filename = "../ui/.streamlit/secrets.toml"
  content = templatefile("${path.module}/template_file/secrets.toml.tmpl", {
    auth0_auth_domain   = var.auth0_domain
    auth0_client_id     = auth0_client.example.client_id
    auth0_client_secret = auth0_client_credentials.example.client_secret
    auth0_audience      = auth0_resource_server.example.identifier
    auth0_redirect_uri  = auth0_client.example.callbacks[0]
    auth0_scope         = "invoke:agent"
  })
}
