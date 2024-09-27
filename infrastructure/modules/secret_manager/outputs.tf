output "openai_api_key_arn" {
  value = data.aws_secretsmanager_secret.openai_api_key.arn
}

output "app_api_key_arn" {
  value = data.aws_secretsmanager_secret.app_api_key.arn
}

output "agent_market_api_key_arn" {
  value = data.aws_secretsmanager_secret.agent_market_api_key.arn
}

output "app_completions_endpoint_arn" {
  value = data.aws_secretsmanager_secret.app_completions_endpoint.arn
}

output "foundation_model_name_secret_arn" {
  value = aws_secretsmanager_secret.foundation_model_name.arn
}

output "aws_bedrock_region_secret_arn" {
  value = aws_secretsmanager_secret.aws_bedrock_region.arn
}
