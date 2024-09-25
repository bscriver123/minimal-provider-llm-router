variable "foundation_model_name" {
  description = "The name of the foundation model"
  type        = string
}

variable "minimal_provider_sg_id" {
  description = "The ID of the security group to allow minimal provider access"
  type        = string
}

variable "subnets" {
  description = "The IDs of the subnets to deploy the ALB to"
  type        = list(string)
}

variable "web_port" {
  description = "The port the web servers are listening on"
  type        = number
}

variable "vpc_id" {
  description = "The ID of the VPC to deploy the ALB to"
  type        = string
}
