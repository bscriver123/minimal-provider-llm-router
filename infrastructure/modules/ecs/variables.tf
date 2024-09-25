variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "foundation_model_name" {
  description = "The name of the foundation model"
  type        = string
}

variable "cpu_architecture" {
  description = "The CPU architecture of the ECS task"
  type        = string
}

variable "web_port" {
  description = "The port the web server listens on"
  type        = number
}

variable "ecr_repository_url" {
  description = "The URL of the ECR repository"
  type        = string
}

variable "docker_image_tag" {
  description = "The tag of the Docker image"
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

variable "public_subnet_ids" {
  description = "The IDs of the public subnets"
  type        = list(string)
}

variable "execution_role_arn" {
  description = "The ARN of the ECS task execution role"
  type        = string
}

variable "task_role_arn" {
  description = "The ARN of the ECS task role"
  type        = string
}

variable "aws_region" {
  description = "The AWS region"
  type        = string
}

variable "alb_target_group_arn" {
  description = "The ARN of the ALB target group"
  type        = string
}

variable "minimal_provider_sg_id" {
  description = "The ID of the security group for the minimal provider"
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
