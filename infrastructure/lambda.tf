# Environment variables shared by every function — table names, index name,
# and log verbosity. Centralized here so we only update it in one place.
locals {
  common_env_vars = {
    EVENTS_TABLE        = aws_dynamodb_table.events.name
    REGISTRATIONS_TABLE = aws_dynamodb_table.registrations.name
    EMAIL_INDEX_NAME    = "email-index"
    LOG_LEVEL           = "INFO"
  }
}

# ---------------------------------------------------------------------------
# list_events_handler
# ---------------------------------------------------------------------------
data "archive_file" "list_events_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build/list_events_handler"
  output_path = "${path.module}/../build/list_events_handler.zip"
}

resource "aws_lambda_function" "list_events" {
  function_name    = "${var.project_name}-${var.environment}-list-events"
  role             = aws_iam_role.list_events_role.arn
  handler          = "app.handler"
  runtime          = var.lambda_runtime
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.list_events_zip.output_path
  source_code_hash = data.archive_file.list_events_zip.output_base64sha256

  environment {
    variables = local.common_env_vars
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "list_events_logs" {
  name              = "/aws/lambda/${aws_lambda_function.list_events.function_name}"
  retention_in_days = 14
}

# ---------------------------------------------------------------------------
# register_handler
# ---------------------------------------------------------------------------
data "archive_file" "register_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build/register_handler"
  output_path = "${path.module}/../build/register_handler.zip"
}

resource "aws_lambda_function" "register" {
  function_name    = "${var.project_name}-${var.environment}-register"
  role             = aws_iam_role.register_role.arn
  handler          = "app.handler"
  runtime          = var.lambda_runtime
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.register_zip.output_path
  source_code_hash = data.archive_file.register_zip.output_base64sha256

  environment {
    variables = merge(local.common_env_vars, {
      CONFIRMATION_TOPIC_ARN = aws_sns_topic.registration_confirmations.arn
    })
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "register_logs" {
  name              = "/aws/lambda/${aws_lambda_function.register.function_name}"
  retention_in_days = 14
}

# ---------------------------------------------------------------------------
# get_registrations_handler
# ---------------------------------------------------------------------------
data "archive_file" "get_registrations_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build/get_registrations_handler"
  output_path = "${path.module}/../build/get_registrations_handler.zip"
}

resource "aws_lambda_function" "get_registrations" {
  function_name    = "${var.project_name}-${var.environment}-get-registrations"
  role             = aws_iam_role.get_registrations_role.arn
  handler          = "app.handler"
  runtime          = var.lambda_runtime
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.get_registrations_zip.output_path
  source_code_hash = data.archive_file.get_registrations_zip.output_base64sha256

  environment {
    variables = local.common_env_vars
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "get_registrations_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_registrations.function_name}"
  retention_in_days = 14
}

# ---------------------------------------------------------------------------
# cancel_registration_handler
# ---------------------------------------------------------------------------
data "archive_file" "cancel_registration_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../build/cancel_registration_handler"
  output_path = "${path.module}/../build/cancel_registration_handler.zip"
}

resource "aws_lambda_function" "cancel_registration" {
  function_name    = "${var.project_name}-${var.environment}-cancel-registration"
  role             = aws_iam_role.cancel_registration_role.arn
  handler          = "app.handler"
  runtime          = var.lambda_runtime
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.cancel_registration_zip.output_path
  source_code_hash = data.archive_file.cancel_registration_zip.output_base64sha256

  environment {
    variables = local.common_env_vars
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "cancel_registration_logs" {
  name              = "/aws/lambda/${aws_lambda_function.cancel_registration.function_name}"
  retention_in_days = 14
}