resource "aws_ecs_cluster" "minimal_provider_cluster" {
  name = "${var.project_name}-cluster"
}

resource "aws_cloudwatch_log_group" "minimal_provider_log_group" {
  name = "/ecs/${var.project_name}-${var.foundation_model_name}"
  retention_in_days = 7  # Set the retention period as per your requirements
}

resource "aws_ecs_task_definition" "minimal_provider_task" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  memory                   = "512"
  cpu                      = "256"
  runtime_platform {
    cpu_architecture       = var.cpu_architecture
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-${var.foundation_model_name}-container"
      image     = "${var.ecr_repository_url}:${var.docker_image_tag}",
      essential = true,
      portMappings = [
        {
          containerPort = var.web_port,
          hostPort      = var.web_port
        }
      ],
      entryPoint = [
        "uvicorn"
      ],
      command = [
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        tostring(var.web_port)
      ],
      environment = [],
      secrets = [
        {
          name      = "OPENAI_API_KEY",
          valueFrom = var.openai_api_key_arn
        },
        {
          name      = "APP_API_KEY",
          valueFrom = var.app_api_key_arn
        },
        {
          name      = "AGENT_MARKET_API_KEY",
          valueFrom = var.agent_market_api_key_arn
        },
        {
          name      = "APP_COMPLETIONS_ENDPOINT",
          valueFrom = var.app_completions_endpoint_arn
        },
        {
            name      = "FOUNDATION_MODEL_NAME",
            valueFrom = var.foundation_model_name_secret_arn
        },
        {
            name      = "AWS_BEDROCK_REGION",
            valueFrom = var.aws_bedrock_region_secret_arn
        },
        {
            name          = "MAX_BID",
            valueFrom     = var.max_bid_secret_arn
        }
      ],
      workingDirectory = "/backend",
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          "awslogs-create-group" = "true",
          "awslogs-group"        = aws_cloudwatch_log_group.minimal_provider_log_group.name,
          "awslogs-region"       = var.aws_region,
          "awslogs-stream-prefix"= "ecs"
        },
        secretOptions = []
      },
      systemControls = []
    }
  ])
}

resource "aws_ecs_service" "minimal_provider_service" {
  name            = "${var.project_name}-${var.foundation_model_name}-service"
  cluster         = aws_ecs_cluster.minimal_provider_cluster.id
  task_definition = aws_ecs_task_definition.minimal_provider_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = var.alb_target_group_arn
    container_name   = "${var.project_name}-${var.foundation_model_name}-container"
    container_port   = var.web_port
  }

  network_configuration {
    subnets         = var.public_subnet_ids
    security_groups = [var.minimal_provider_sg_id]
    assign_public_ip = true
  }
}
