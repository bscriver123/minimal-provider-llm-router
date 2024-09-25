data "aws_ecr_repository" "repository" {
  name = var.ecr_repository_name
}
