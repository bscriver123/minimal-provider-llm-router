variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "openai_api_key_arn" {
  description = "The ARN of the secret for the OpenAI API key"
  type        = string
}

variable "anthropic_api_key_arn" {
  description = "The ARN of the secret for the Anthropic API key"
  type        = string
}

variable "notdiamond_api_key_arn" {
  description = "The ARN of the secret for the notdiamond API key"
  type        = string
}

variable "market_api_key_arn" {
  description = "The ARN of the secret for the market API key"
  type        = string
}

variable "app_completions_endpoint_arn" {
  description = "The ARN of the secret for the app completions endpoint"
  type        = string
}
