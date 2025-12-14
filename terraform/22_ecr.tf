###############################################################################
# Amazon ECR                                                                  #
###############################################################################
resource "aws_ecr_repository" "example" {
  name                 = local.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  force_delete = true

}

ephemeral "aws_ecr_authorization_token" "token" {}

resource "terraform_data" "image_push" {
  triggers_replace = {
    template_hash = sha256(
      join(
        "",
        concat(
          [for rel in sort(fileset("../agents/src/agents", "**")) : filesha256("../agents/src/agents/${rel}")],
        )
      )
    )
  }

  provisioner "local-exec" {
    command = <<-EOF
      docker buildx build --platform linux/arm64 ../agents -t ${aws_ecr_repository.example.repository_url}:latest; \
      docker login -u AWS -p ${ephemeral.aws_ecr_authorization_token.token.password} ${ephemeral.aws_ecr_authorization_token.token.proxy_endpoint}; \
      docker push ${aws_ecr_repository.example.repository_url}:latest
    EOF
  }
}
