data "aws_vpcs" "existing_vpcs" {
  filter {
    name   = "tag:Name"
    values = ["${var.project_name}-vpc"]
  }
}

data "aws_subnets" "existing_vpc_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpcs.existing_vpcs.ids[0]]
  }
}
