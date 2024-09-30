#!/bin/bash

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
CPU_ARCHITECTURE=$(uname -m | tr '[:lower:]' '[:upper:]')
AWS_REGION=$(aws configure get region)

source .env

export DOCKER_IMAGE_TAG=$(date +'%Y%m%d%H%M%S')-$PROJECT_NAME-llm-router
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
docker build . --no-cache -t "$PROJECT_NAME-repo:$DOCKER_IMAGE_TAG"
docker tag "$PROJECT_NAME-repo:$DOCKER_IMAGE_TAG" "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$PROJECT_NAME-repo:$DOCKER_IMAGE_TAG"
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$PROJECT_NAME-repo:$DOCKER_IMAGE_TAG"

cd infrastructure
terraform init

workspace_name=$PROJECT_NAME-llm-router-$CPU_ARCHITECTURE

if terraform workspace list | grep -q -w "$workspace_name"; then
  echo "Workspace $workspace_name exists. Selecting it..."
else
  echo "Workspace $workspace_name does not exist. Creating and selecting it..."
  terraform workspace new "$workspace_name"
fi

terraform workspace select "$workspace_name"

terraform plan \
  --var "docker_image_tag=$DOCKER_IMAGE_TAG" \
  --var "aws_region=$AWS_REGION" \
  --var "project_name=$PROJECT_NAME" \
  --var "cpu_architecture=$CPU_ARCHITECTURE"

terraform apply \
  --var "docker_image_tag=$DOCKER_IMAGE_TAG" \
  --var "aws_region=$AWS_REGION" \
  --var "project_name=$PROJECT_NAME" \
  --var "cpu_architecture=$CPU_ARCHITECTURE"
