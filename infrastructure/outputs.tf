output "events_table_name" {
  description = "Name of the DynamoDB events table"
  value       = aws_dynamodb_table.events.name
}

output "registrations_table_name" {
  description = "Name of the DynamoDB registrations table"
  value       = aws_dynamodb_table.registrations.name
}

output "lambda_function_names" {
  description = "Names of all deployed Lambda functions"
  value = {
    list_events          = aws_lambda_function.list_events.function_name
    register             = aws_lambda_function.register.function_name
    get_registrations    = aws_lambda_function.get_registrations.function_name
    cancel_registration  = aws_lambda_function.cancel_registration.function_name
  }
}