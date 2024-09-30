data "aws_secretsmanager_secret" "openai_api_key" {
  name = "${var.project_name}-llm-router-openai-api-key"
}

data "aws_secretsmanager_secret" "anthropic_api_key" {
  name = "${var.project_name}-llm-router-anthropic-api-key"
}

data "aws_secretsmanager_secret" "notdiamond_api_key" {
  name = "${var.project_name}-llm-router-notdiamond-api-key"
}

data "aws_secretsmanager_secret" "market_api_key" {
  name = "${var.project_name}-llm-router-market-api-key"
}

data "aws_secretsmanager_secret" "app_completions_endpoint" {
  name = "${var.project_name}-llm-router-app-completions-endpoint"
}
