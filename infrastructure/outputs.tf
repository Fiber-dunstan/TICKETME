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
    list_events         = aws_lambda_function.list_events.function_name
    register            = aws_lambda_function.register.function_name
    get_registrations   = aws_lambda_function.get_registrations.function_name
    cancel_registration = aws_lambda_function.cancel_registration.function_name
  }
}

output "api_base_url" {
  description = "Base URL for the TicketMe REST API"
  value       = aws_api_gateway_stage.dev.invoke_url
}

output "frontend_bucket_name" {
  description = "S3 bucket name for frontend static files"
  value       = aws_s3_bucket.frontend.id
}

output "frontend_url" {
  description = "Public HTTPS URL for the deployed frontend"
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID, used for cache invalidation on deploy"
  value       = aws_cloudfront_distribution.frontend.id
}