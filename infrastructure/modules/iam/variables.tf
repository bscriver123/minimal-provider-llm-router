variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "foundation_model_name" {
  description = "The name of the foundation model"
  type        = string
}

variable "openai_api_key_arn" {
  description = "The ARN of the secret for the OpenAI API key"
  type        = string
}

variable "app_api_key_arn" {
  description = "The ARN of the secret for the app API key"
  type        = string
}

variable "agent_market_api_key_arn" {
  description = "The ARN of the secret for the agent market API key"
  type        = string
}

variable "app_completions_endpoint_arn" {
  description = "The ARN of the secret for the app completions endpoint"
  type        = string
}

variable "max_bid_secret_arn" {
  description = "The ARN of the secret for the max bid"
  type        = string
}

variable "foundation_model_name_secret_arn" {
  description = "The ARN of the secret for the foundation model name"
  type        = string
}

variable "aws_bedrock_region_secret_arn" {
  description = "The ARN of the secret for the AWS Bedrock region"
  type        = string
}
