"""
TicketMe - Register Handler Lambda
Handles: POST /register
Creates a new event registration, enforcing validation, duplicate prevention,
and capacity limits.
"""
import os
import sys
import json
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "shared"))

from response_utils import build_response  # noqa: E402
from logger import get_logger  # noqa: E402
from validators import validate_registration_input  # noqa: E402

logger = get_logger(__name__)
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

EVENTS_TABLE_NAME = os.environ.get("EVENTS_TABLE", "ticketme-events")
REGISTRATIONS_TABLE_NAME = os.environ.get("REGISTRATIONS_TABLE", "ticketme-registrations")
EMAIL_INDEX_NAME = os.environ.get("EMAIL_INDEX_NAME", "email-index")
CONFIRMATION_TOPIC_ARN = os.environ.get("CONFIRMATION_TOPIC_ARN")


def handler(event, context):
    logger.info("Received registration request")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return build_response(400, {"error": "Request body must be valid JSON."})

    errors, clean = validate_registration_input(body)
    if errors:
        return build_response(400, {"error": "Validation failed", "details": errors})

    events_table = dynamodb.Table(EVENTS_TABLE_NAME)
    registrations_table = dynamodb.Table(REGISTRATIONS_TABLE_NAME)

    # 1. Confirm the event exists
    event_result = events_table.get_item(Key={"eventId": clean["eventId"]})
    event_item = event_result.get("Item")
    if not event_item:
        return build_response(404, {"error": "Event not found."})

    # 2. Prevent duplicate registrations for the same email + event
    existing = registrations_table.query(
        IndexName=EMAIL_INDEX_NAME,
        KeyConditionExpression=Key("email").eq(clean["email"]),
    )
    for item in existing.get("Items", []):
        if item.get("eventId") == clean["eventId"] and item.get("status") == "CONFIRMED":
            return build_response(409, {"error": "You are already registered for this event."})

    # 3. Atomically reserve a seat (fails safely if event is full).
    # Note: "capacity" is a DynamoDB reserved keyword, so we must reference it
    # via an ExpressionAttributeNames placeholder (#cap) rather than directly.
    try:
        events_table.update_item(
            Key={"eventId": clean["eventId"]},
            UpdateExpression="SET registeredCount = registeredCount + :inc",
            ConditionExpression="registeredCount < #cap",
            ExpressionAttributeNames={"#cap": "capacity"},
            ExpressionAttributeValues={":inc": 1},
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return build_response(409, {"error": "This event is fully booked."})
        logger.error(f"Unexpected DynamoDB error reserving seat: {e}")
        return build_response(500, {"error": "Failed to process registration."})

    # 4. Create the registration record
    registration_id = str(uuid.uuid4())
    ticket_code = str(uuid.uuid4())[:8].upper()
    now = datetime.now(timezone.utc).isoformat()

    registration_item = {
        "registrationId": registration_id,
        "eventId": clean["eventId"],
        "email": clean["email"],
        "fullName": clean["fullName"],
        "phoneNumber": clean["phoneNumber"],
        "status": "CONFIRMED",
        "registeredAt": now,
        "ticketCode": ticket_code,
    }

    try:
        registrations_table.put_item(Item=registration_item)
    except ClientError as e:
        # Compensating action: undo the seat reservation since we couldn't
        # actually save the registration record.
        logger.error(f"Failed to save registration, rolling back seat count: {e}")
        events_table.update_item(
            Key={"eventId": clean["eventId"]},
            UpdateExpression="SET registeredCount = registeredCount - :dec",
            ExpressionAttributeValues={":dec": 1},
        )
        return build_response(500, {"error": "Failed to complete registration. Please try again."})

    logger.info(f"Registration created: {registration_id} for event {clean['eventId']}")

    # Best-effort notification: we don't want an SNS hiccup to fail an
    # otherwise-successful registration, so we log and continue on error
    # rather than returning a 500 to the user at this point.
    if CONFIRMATION_TOPIC_ARN:
        try:
            sns.publish(
                TopicArn=CONFIRMATION_TOPIC_ARN,
                Subject="TicketMe Registration Confirmed",
                Message=(
                    f"Hi {clean['fullName']},\n\n"
                    f"You're confirmed for event {clean['eventId']}.\n"
                    f"Your ticket code is: {ticket_code}\n\n"
                    f"See you there!\n— TicketMe"
                ),
            )
        except ClientError as e:
            logger.error(f"Failed to publish SNS confirmation: {e}")

    return build_response(201, {"message": "Registration successful", "registration": registration_item})