output "events_table_name" {
  description = "Name of the DynamoDB events table"
  value       = aws_dynamodb_table.events.name
}

output "registrations_table_name" {
  description = "Name of the DynamoDB registrations table"
  value       = aws_dynamodb_table.registrations.name
}