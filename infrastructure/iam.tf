# ---------------------------------------------------------------------------
# Trust policy shared by every Lambda role: allows the Lambda *service*
# (not a person) to assume the role.
# ---------------------------------------------------------------------------
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Basic CloudWatch Logs permissions, shared by every function.
data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

# =============================================================================
# list_events_handler — read-only access to Events table
# =============================================================================
resource "aws_iam_role" "list_events_role" {
  name               = "${var.project_name}-${var.environment}-list-events-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "list_events_policy" {
  statement {
    effect    = "Allow"
    actions   = ["dynamodb:Scan"]
    resources = [aws_dynamodb_table.events.arn]
  }
}

resource "aws_iam_role_policy" "list_events_dynamodb" {
  name   = "dynamodb-access"
  role   = aws_iam_role.list_events_role.id
  policy = data.aws_iam_policy_document.list_events_policy.json
}

resource "aws_iam_role_policy" "list_events_logging" {
  name   = "logging"
  role   = aws_iam_role.list_events_role.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

# =============================================================================
# register_handler — read/update Events (capacity check + seat reservation),
# read/write Registrations (duplicate check + create)
# =============================================================================
resource "aws_iam_role" "register_role" {
  name               = "${var.project_name}-${var.environment}-register-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "register_policy" {
  statement {
    effect    = "Allow"
    actions   = ["dynamodb:GetItem", "dynamodb:UpdateItem"]
    resources = [aws_dynamodb_table.events.arn]
  }

  statement {
    effect  = "Allow"
    actions = ["dynamodb:PutItem", "dynamodb:Query"]
    resources = [
      aws_dynamodb_table.registrations.arn,
      "${aws_dynamodb_table.registrations.arn}/index/email-index",
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.registration_confirmations.arn]
  }
}

resource "aws_iam_role_policy" "register_dynamodb" {
  name   = "dynamodb-access"
  role   = aws_iam_role.register_role.id
  policy = data.aws_iam_policy_document.register_policy.json
}

resource "aws_iam_role_policy" "register_logging" {
  name   = "logging"
  role   = aws_iam_role.register_role.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

# =============================================================================
# get_registrations_handler — Query-only via the email-index GSI
# =============================================================================
resource "aws_iam_role" "get_registrations_role" {
  name               = "${var.project_name}-${var.environment}-get-registrations-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "get_registrations_policy" {
  statement {
    effect  = "Allow"
    actions = ["dynamodb:Query"]
    resources = [
      aws_dynamodb_table.registrations.arn,
      "${aws_dynamodb_table.registrations.arn}/index/email-index",
    ]
  }
}

resource "aws_iam_role_policy" "get_registrations_dynamodb" {
  name   = "dynamodb-access"
  role   = aws_iam_role.get_registrations_role.id
  policy = data.aws_iam_policy_document.get_registrations_policy.json
}

resource "aws_iam_role_policy" "get_registrations_logging" {
  name   = "logging"
  role   = aws_iam_role.get_registrations_role.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

# =============================================================================
# cancel_registration_handler — read/update Registrations, update Events
# (to free up a seat)
# =============================================================================
resource "aws_iam_role" "cancel_registration_role" {
  name               = "${var.project_name}-${var.environment}-cancel-registration-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "cancel_registration_policy" {
  statement {
    effect    = "Allow"
    actions   = ["dynamodb:GetItem", "dynamodb:UpdateItem"]
    resources = [aws_dynamodb_table.registrations.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["dynamodb:UpdateItem"]
    resources = [aws_dynamodb_table.events.arn]
  }
}

resource "aws_iam_role_policy" "cancel_registration_dynamodb" {
  name   = "dynamodb-access"
  role   = aws_iam_role.cancel_registration_role.id
  policy = data.aws_iam_policy_document.cancel_registration_policy.json
}

resource "aws_iam_role_policy" "cancel_registration_logging" {
  name   = "logging"
  role   = aws_iam_role.cancel_registration_role.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}