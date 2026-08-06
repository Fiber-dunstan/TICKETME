# =============================================================================
# REST API
# =============================================================================
resource "aws_api_gateway_rest_api" "ticketme" {
  name        = "${var.project_name}-${var.environment}-api"
  description = "TicketMe Event Registration & Ticketing REST API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# =============================================================================
# /events  (GET -> list_events)
# =============================================================================
resource "aws_api_gateway_resource" "events" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_rest_api.ticketme.root_resource_id
  path_part   = "events"
}

resource "aws_api_gateway_method" "get_events" {
  rest_api_id   = aws_api_gateway_rest_api.ticketme.id
  resource_id   = aws_api_gateway_resource.events.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_events" {
  rest_api_id             = aws_api_gateway_rest_api.ticketme.id
  resource_id             = aws_api_gateway_resource.events.id
  http_method             = aws_api_gateway_method.get_events.http_method
  integration_http_method = "POST" # Lambda integrations are always invoked via POST internally
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.list_events.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_list_events" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_events.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ticketme.execution_arn}/*/*"
}

# =============================================================================
# /register  (POST -> register)
# =============================================================================
resource "aws_api_gateway_resource" "register" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_rest_api.ticketme.root_resource_id
  path_part   = "register"
}

resource "aws_api_gateway_method" "post_register" {
  rest_api_id   = aws_api_gateway_rest_api.ticketme.id
  resource_id   = aws_api_gateway_resource.register.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_register" {
  rest_api_id             = aws_api_gateway_rest_api.ticketme.id
  resource_id             = aws_api_gateway_resource.register.id
  http_method             = aws_api_gateway_method.post_register.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.register.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_register" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.register.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ticketme.execution_arn}/*/*"
}

# =============================================================================
# /registrations/{email}  (GET -> get_registrations)
# =============================================================================
resource "aws_api_gateway_resource" "registrations" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_rest_api.ticketme.root_resource_id
  path_part   = "registrations"
}

resource "aws_api_gateway_resource" "registrations_email" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_resource.registrations.id
  path_part   = "{email}"
}

resource "aws_api_gateway_method" "get_registrations" {
  rest_api_id   = aws_api_gateway_rest_api.ticketme.id
  resource_id   = aws_api_gateway_resource.registrations_email.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.email" = true
  }
}

resource "aws_api_gateway_integration" "get_registrations" {
  rest_api_id             = aws_api_gateway_rest_api.ticketme.id
  resource_id             = aws_api_gateway_resource.registrations_email.id
  http_method             = aws_api_gateway_method.get_registrations.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.get_registrations.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_get_registrations" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_registrations.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ticketme.execution_arn}/*/*"
}

# =============================================================================
# /registration/{id}  (DELETE -> cancel_registration)
# =============================================================================
resource "aws_api_gateway_resource" "registration" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_rest_api.ticketme.root_resource_id
  path_part   = "registration"
}

resource "aws_api_gateway_resource" "registration_id" {
  rest_api_id = aws_api_gateway_rest_api.ticketme.id
  parent_id   = aws_api_gateway_resource.registration.id
  path_part   = "{id}"
}

resource "aws_api_gateway_method" "delete_registration" {
  rest_api_id   = aws_api_gateway_rest_api.ticketme.id
  resource_id   = aws_api_gateway_resource.registration_id.id
  http_method   = "DELETE"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.id" = true
  }
}

resource "aws_api_gateway_integration" "delete_registration" {
  rest_api_id             = aws_api_gateway_rest_api.ticketme.id
  resource_id             = aws_api_gateway_resource.registration_id.id
  http_method             = aws_api_gateway_method.delete_registration.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cancel_registration.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_cancel_registration" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cancel_registration.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ticketme.execution_arn}/*/*"
}