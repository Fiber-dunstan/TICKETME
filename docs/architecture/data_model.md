# TicketMe – Data Model & Architecture

## Overview

TicketMe uses two DynamoDB tables designed around the application's specific access patterns, following DynamoDB best practices (design for queries, not for normalized structure).

## Table: ticketme-dev-events

| Attribute | Type | Key |
|---|---|---|
| eventId | String (UUID) | Partition Key |
| eventName | String | |
| description | String | |
| category | String | |
| eventDate | String (ISO 8601) | |
| location | String | |
| capacity | Number | |
| registeredCount | Number | |
| createdAt | String (ISO 8601) | |

Billing mode: `PAY_PER_REQUEST` (Free Tier friendly — no idle cost).

## Table: ticketme-dev-registrations

| Attribute | Type | Key |
|---|---|---|
| registrationId | String (UUID) | Partition Key |
| eventId | String | |
| email | String | |
| fullName | String | |
| phoneNumber | String | |
| status | String (CONFIRMED / CANCELLED) | |
| registeredAt | String (ISO 8601) | |
| ticketCode | String | |

### Global Secondary Index: email-index
- Partition Key: `email`
- Projection: `ALL`
- Purpose: Efficiently fetch all registrations for a given user without scanning the full table.

## Access Patterns Covered

| # | Action | Query |
|---|---|---|
| 1 | List all events | `Scan` on `ticketme-dev-events` |
| 2 | Register for an event | `GetItem` (event exists check) → `Query` via `email-index` (duplicate check) → `UpdateItem` with `ConditionExpression` (atomic capacity check + seat reservation) → `PutItem` (create registration) |
| 3 | View a user's registrations | `Query` on `ticketme-dev-registrations` via `email-index` |
| 4 | Cancel a registration | `GetItem` (existence/status check) → `UpdateItem` (soft-delete: status → CANCELLED) → `UpdateItem` on events table (free the seat) |

## Design Decisions

- **Two tables, not single-table design.** DynamoDB's advanced "single-table design" pattern was deliberately not used — it adds complexity that isn't justified at this project's scale, and would reduce code readability for a reviewer. Documented as a future improvement.
- **`registeredCount` maintained on the event item** (rather than counting registrations on read) to allow fast, atomic capacity checks via DynamoDB conditional updates, avoiding the need to scan/count registrations on every request.
- **Concurrency safety**: seat reservation uses `ConditionExpression = "registeredCount < capacity"` on an atomic `UpdateItem` call, preventing overselling even under simultaneous registration requests — DynamoDB rejects the write outright if the condition fails, rather than us reading-then-writing non-atomically.
- **Soft deletes for cancellations** (`status = CANCELLED` rather than removing the item) to preserve an audit trail and support future analytics/reporting.
- **`ExpressionAttributeNames` placeholders** used for any DynamoDB reserved keyword (`capacity`, `status`) in expressions, to avoid `ValidationException` errors.

## Supporting Infrastructure

| Component | Purpose |
|---|---|
| IAM | One role per Lambda function, least-privilege — e.g. `list_events` can only `Scan`; `get_registrations` can only `Query` the GSI |
| CloudWatch Logs | Per-function log groups, 14-day retention |
| CloudWatch Alarms | Error rate (`errors ÷ invocations × 100`) per function, alarming above 5%, notifying via SNS |
| SNS — Ops Alerts | Subscribed operator email, notified on alarm state changes and on each new registration |
| AWS Budgets | Monthly cost alert at 80% actual / 100% forecasted spend |
| S3 + CloudFront | Private S3 bucket (Origin Access Control), CloudFront for HTTPS/CDN/SPA routing |
| GitHub Actions | Automated test suite + Terraform validation on every push/PR, enforced via branch protection |