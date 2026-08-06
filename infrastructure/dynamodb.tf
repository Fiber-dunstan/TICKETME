# ---------------------------------------------------------------------------
# Events Table
# Stores event details. Partition key only — events are looked up
# individually by ID or listed in full (scan).
# ---------------------------------------------------------------------------
resource "aws_dynamodb_table" "events" {
  name         = "${var.project_name}-${var.environment}-events"
  billing_mode = "PAY_PER_REQUEST" # Free-tier friendly: pay only for actual usage, no idle cost
  hash_key     = "eventId"

  attribute {
    name = "eventId"
    type = "S" # S = String
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# ---------------------------------------------------------------------------
# Registrations Table
# Stores registration records. Partition key is registrationId (used for
# cancellation lookups). A Global Secondary Index on "email" lets us
# efficiently fetch all registrations belonging to one user.
# ---------------------------------------------------------------------------
resource "aws_dynamodb_table" "registrations" {
  name         = "${var.project_name}-${var.environment}-registrations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "registrationId"

  attribute {
    name = "registrationId"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL" # Include all item attributes in the index (simplest, fine at our scale)
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}