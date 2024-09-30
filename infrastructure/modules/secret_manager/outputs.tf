output "openai_api_key_arn" {
  value = data.aws_secretsmanager_secret.openai_api_key.arn
}

output "anthropic_api_key_arn" {
  value = data.aws_secretsmanager_secret.anthropic_api_key.arn
}

output "notdiamond_api_key_arn" {
  value = data.aws_secretsmanager_secret.notdiamond_api_key.arn
}

output "market_api_key_arn" {
  value = data.aws_secretsmanager_secret.market_api_key.arn
}

output "app_completions_endpoint_arn" {
  value = data.aws_secretsmanager_secret.app_completions_endpoint.arn
}
