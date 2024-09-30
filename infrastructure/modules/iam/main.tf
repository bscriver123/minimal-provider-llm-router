resource "aws_iam_role" "ecs_execution_role" {
  name = "ecsExecutionRole${var.project_name}-llm-router"
  description = "Role for ECS execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ],
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "ecsTaskRole${var.project_name}-llm-router"
  description = "Role for ECS tasks"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ],
  })
}

resource "aws_iam_policy" "cloudwatch_logs_policy" {
  name = "CloudWatchLogsPolicy${var.project_name}-llm-router"
  description = "Policy for CloudWatch Logs"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_policy" "ecr_access_policy" {
  name = "ECRAccessPolicy-${var.project_name}-llm-router"
  description = "Policy for ECR access"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "secrets_manager_policy" {
  name = "SecretsManagerPolicy${var.project_name}-llm-router"
  description = "Policy for ECS tasks"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Resource = [
          var.openai_api_key_arn,
          var.anthropic_api_key_arn,
          var.notdiamond_api_key_arn,
          var.market_api_key_arn,
          var.app_completions_endpoint_arn,
        ]
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "ecs_execution_policy_attachment" {
  name       = "ecsExecutionRolePolicyAttachment"
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy_attachment" "cloudwatch_logs_policy_attachment" {
  name       = "ecsExecutionRoleCloudWatchLogsPolicyAttachment"
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = aws_iam_policy.cloudwatch_logs_policy.arn
}

resource "aws_iam_policy_attachment" "ecr_access_policy_attachment" {
  name       = "ecsExecutionRoleECRAccessPolicyAttachment"
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = aws_iam_policy.ecr_access_policy.arn
}

resource "aws_iam_policy_attachment" "secrets_manager_policy_attachment" {
  name       = "ecsExecutionRoleSecretsManagerPolicyAttachment"
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}
