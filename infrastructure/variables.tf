variable "docker_image_tag" {
  description = "The name of the Docker image"
  type        = string
}

variable "aws_region" {
  description = "The AWS region"
  type        = string
  default     = "eu-west-1" # Change if necessary
}

variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "minimal-provider" # Change if necessary
}

variable "cpu_architecture" {
  description = "The CPU architecture of the ECS task"
  type        = string
  default     = "ARM64" # Change if necessary
}

variable "web_port" {
  description = "The port the web server listens on"
  type        = number
  default     = 80 # Change if necessary
}

variable "openai_api_key_secret_name" {
  description = "The name of the secret for the OpenAI API key"
  type        = string
  default     = "OPEN_AI_API_KEY"
}

variable "anthropic_api_key_secret_name" {
  description = "The name of the secret for the Anthropic API key"
  type        = string
  default     = "ANTHROPIC_API_KEY"
}

variable "notdiamond_api_key_secret_name" {
  description = "The name of the secret for the notdiamond API key"
  type        = string
  default     = "NOTDIAMOND_API_KEY"
}

variable "market_api_key_secret_name" {
  description = "The name of the secret for the market API key"
  type        = string
  default     = "MARKET_API_KEY"
}

variable "app_completions_endpoint_secret_name" {
  description = "The name of the secret for the app completions endpoint"
  type        = string
  default     = "APP_COMPLETIONS_ENDPOINT"
}
