data "aws_secretsmanager_secret" "openai_api_key" {
  name = "${var.project_name}-${var.foundation_model_name}-openai-api-key"
}

data "aws_secretsmanager_secret" "app_api_key" {
  name = "${var.project_name}-${var.foundation_model_name}-app-api-key"
}

data "aws_secretsmanager_secret" "agent_market_api_key" {
  name = "${var.project_name}-${var.foundation_model_name}-agent-market-api-key"
}

data "aws_secretsmanager_secret" "app_completions_endpoint" {
  name = "${var.project_name}-${var.foundation_model_name}-app-completions-endpoint"
}

resource "aws_secretsmanager_secret" "foundation_model_name" {
  name        = "${var.project_name}-${var.foundation_model_name}-foundation-model-name"
  description = "The name of the foundation model for the project"
}

resource "aws_secretsmanager_secret_version" "foundation_model_value" {
  secret_id     = aws_secretsmanager_secret.foundation_model_name.id
  secret_string = var.foundation_model_name
}

resource "aws_secretsmanager_secret" "aws_bedrock_region" {
  name        = "${var.project_name}-${var.foundation_model_name}-aws-bedrock-region"
  description = "The AWS region where the Bedrock infrastructure is deployed"
}

resource "aws_secretsmanager_secret_version" "aws_bedrock_region_value" {
  secret_id     = aws_secretsmanager_secret.aws_bedrock_region.id
  secret_string = var.aws_bedrock_region
}
