variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "max_bid" {
  description = "The maximum bid for completions"
  type        = string
}

variable "foundation_model_name" {
  description = "The name of the foundation model"
  type        = string
}

variable "aws_bedrock_region" {
  description = "The AWS region where the Bedrock infrastructure is deployed"
  type        = string
}
