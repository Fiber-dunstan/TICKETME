variable "aws_region" {
  description = "AWS region to deploy TicketMe resources into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used as a prefix for resource naming"
  type        = string
  default     = "ticketme"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "lambda_runtime" {
  description = "Python runtime version for all Lambda functions"
  type        = string
  default     = "python3.12"
}

variable "alert_email" {
  description = "Email address to receive operational alerts and registration confirmations"
  type        = string
}

variable "monthly_budget_limit" {
  description = "Monthly AWS spending limit (USD) before budget alerts fire"
  type        = string
  default     = "5"
}