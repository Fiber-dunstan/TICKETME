# =============================================================================
# Error-rate alarms — one per Lambda function. Uses a metric math expression
# to calculate errors as a percentage of invocations, alarming if it exceeds
# 5% (per the capstone requirement), evaluated over a 5-minute window.
# =============================================================================
locals {
  monitored_functions = {
    list_events         = aws_lambda_function.list_events.function_name
    register            = aws_lambda_function.register.function_name
    get_registrations   = aws_lambda_function.get_registrations.function_name
    cancel_registration = aws_lambda_function.cancel_registration.function_name
  }
}

resource "aws_cloudwatch_metric_alarm" "error_rate" {
  for_each = local.monitored_functions

  alarm_name          = "${var.project_name}-${var.environment}-${each.key}-error-rate-high"
  alarm_description   = "Triggers when ${each.key} Lambda error rate exceeds 5% over 5 minutes"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 5
  evaluation_periods  = 1
  treat_missing_data  = "notBreaching" # No invocations = no problem, don't false-alarm

  metric_query {
    id          = "error_rate"
    expression  = "(errors / invocations) * 100"
    label       = "Error Rate (%)"
    return_data = true
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = 300
      stat        = "Sum"
      dimensions = {
        FunctionName = each.value
      }
    }
  }

  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = 300
      stat        = "Sum"
      dimensions = {
        FunctionName = each.value
      }
    }
  }

  alarm_actions = [aws_sns_topic.ops_alerts.arn]
  ok_actions    = [aws_sns_topic.ops_alerts.arn]
}