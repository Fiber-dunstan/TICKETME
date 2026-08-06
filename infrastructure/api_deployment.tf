resource "aws_api_gateway_deployment" "ticketme" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id

  # Forces a new deployment whenever any part of the API definition changes -
  # otherwise Terraform might not realize a redeploy is needed.
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.events.id,
      aws_api_gateway_method.get_events.id,
      aws_api_gateway_integration.get_events.id,
      aws_api_gateway_resource.register.id,
      aws_api_gateway_method.post_register.id,
      aws_api_gateway_integration.post_register.id,
      aws_api_gateway_resource.registrations_email.id,
      aws_api_gateway_method.get_registrations.id,
      aws_api_gateway_integration.get_registrations.id,
      aws_api_gateway_resource.registration_id.id,
      aws_api_gateway_method.delete_registration.id,
      aws_api_gateway_integration.delete_registration.id,
      aws_api_gateway_method.options,
      aws_api_gateway_integration.options,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.ticketme.id
  rest_api_id   = aws_api_gateway_rest_api.ticketme.id
  stage_name    = var.environment
}