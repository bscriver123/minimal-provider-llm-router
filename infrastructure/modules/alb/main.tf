resource "aws_lb" "app_lb" {
  name               = "lb-llm-router"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.minimal_provider_sg_id]
  subnets            = var.subnets

  enable_deletion_protection = true
}

resource "aws_lb_target_group" "app_tg" {
  name     = "tg-llm-router"
  port     = var.web_port
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  target_type = "ip"

  health_check {
    interval            = 30
    path                = "/v1/completions/healthcheck"
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
    matcher             = "200"
  }
}

resource "aws_lb_listener" "app_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = "${var.web_port}"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}
