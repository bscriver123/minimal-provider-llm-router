variable "docker_image_tag" {
  description = "The name of the Docker image"
  type        = string
}

variable "aws_region" {
  description = "The AWS region"
  type        = string
  default     = "eu-west-1" # Change if necessary
}

variable "aws_bedrock_region" {
  description = "The AWS region to pull Bedrock resources from"
  type        = string
}

variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "minimal-provider" # Change if necessary
}

variable "foundation_model_name" {
  description = "The name of the foundation model"
  type        = string
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

variable "app_api_key_secret_name" {
  description = "The name of the secret for the app API key"
  type        = string
  default     = "APP_API_KEY"
}

variable "agent_market_api_key_secret_name" {
  description = "The name of the secret for the agent market API key"
  type        = string
  default     = "AGENT_MARKET_API_KEY"
}

variable "app_completions_endpoint_secret_name" {
  description = "The name of the secret for the app completions endpoint"
  type        = string
  default     = "APP_COMPLETIONS_ENDPOINT"
}

variable "max_bid" {
  description = "The maximum bid for the agent market"
  type        = string
}