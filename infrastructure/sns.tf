# =============================================================================
# Operational Alerts Topic — CloudWatch alarms publish here (e.g. high error
# rate). Subscribe your own email to get notified when something breaks.
# =============================================================================
resource "aws_sns_topic" "ops_alerts" {
  name = "${var.project_name}-${var.environment}-ops-alerts"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_sns_topic_subscription" "ops_alerts_email" {
  topic_arn = aws_sns_topic.ops_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# =============================================================================
# Registration Confirmations Topic — the register Lambda publishes here
# whenever someone successfully registers, so we can email them a
# confirmation (optional feature called out in the capstone brief).
# =============================================================================
resource "aws_sns_topic" "registration_confirmations" {
  name = "${var.project_name}-${var.environment}-registration-confirmations"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}