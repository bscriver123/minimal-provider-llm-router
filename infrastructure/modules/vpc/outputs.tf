output "vpc_id" {
  value = data.aws_vpcs.existing_vpcs.ids[0]
}

output "subnet_ids" {
  value = data.aws_subnets.existing_vpc_subnets.ids
}