"""
TicketMe - Cancel Registration Handler Lambda
Handles: DELETE /registration/{id}
Soft-cancels a registration (status -> CANCELLED) and frees up a seat on the
associated event.
"""
import os
import sys
from urllib.parse import unquote
import boto3
from botocore.exceptions import ClientError

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "shared"))

from response_utils import build_response  # noqa: E402
from logger import get_logger  # noqa: E402

logger = get_logger(__name__)
dynamodb = boto3.resource("dynamodb")

EVENTS_TABLE_NAME = os.environ.get("EVENTS_TABLE", "ticketme-events")
REGISTRATIONS_TABLE_NAME = os.environ.get("REGISTRATIONS_TABLE", "ticketme-registrations")


def handler(event, context):
    logger.info("Received request to cancel a registration")

    path_params = event.get("pathParameters") or {}
    registration_id = unquote(path_params.get("id") or "").strip()

    if not registration_id:
        return build_response(400, {"error": "Registration id is required in the URL path."})

    registrations_table = dynamodb.Table(REGISTRATIONS_TABLE_NAME)
    events_table = dynamodb.Table(EVENTS_TABLE_NAME)

    # 1. Confirm the registration exists
    existing = registrations_table.get_item(Key={"registrationId": registration_id})
    item = existing.get("Item")
    if not item:
        return build_response(404, {"error": "Registration not found."})

    if item.get("status") == "CANCELLED":
        return build_response(409, {"error": "This registration is already cancelled."})

    # 2. Mark it cancelled (soft delete, preserves audit trail)
    try:
        registrations_table.update_item(
            Key={"registrationId": registration_id},
            UpdateExpression="SET #s = :cancelled",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":cancelled": "CANCELLED"},
        )
    except ClientError as e:
        logger.error(f"Failed to cancel registration {registration_id}: {e}")
        return build_response(500, {"error": "Failed to cancel registration. Please try again."})

    # 3. Free up the seat on the event (best-effort; registration is already
    # cancelled at this point, so we log but don't fail the request if this
    # step has an issue).
    try:
        events_table.update_item(
            Key={"eventId": item["eventId"]},
            UpdateExpression="SET registeredCount = registeredCount - :dec",
            ConditionExpression="registeredCount > :zero",
            ExpressionAttributeValues={":dec": 1, ":zero": 0},
        )
    except ClientError as e:
        logger.error(f"Could not decrement seat count for event {item['eventId']}: {e}")

    logger.info(f"Registration {registration_id} cancelled successfully")
    return build_response(200, {"message": "Registration cancelled successfully."})