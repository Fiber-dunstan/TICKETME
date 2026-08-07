"""
TicketMe - Get Registrations Handler Lambda
Handles: GET /registrations/{email}
Returns all registrations (any status) belonging to the given email address.
"""
import os
import sys
from urllib.parse import unquote
import boto3
from boto3.dynamodb.conditions import Key

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "shared"))

from response_utils import build_response  # noqa: E402
from logger import get_logger  # noqa: E402

logger = get_logger(__name__)
dynamodb = boto3.resource("dynamodb")

REGISTRATIONS_TABLE_NAME = os.environ.get("REGISTRATIONS_TABLE", "ticketme-registrations")
EMAIL_INDEX_NAME = os.environ.get("EMAIL_INDEX_NAME", "email-index")


def handler(event, context):
    logger.info("Received request to fetch registrations by email")

    path_params = event.get("pathParameters") or {}
    email = unquote(path_params.get("email") or "").strip().lower()

    if not email:
        return build_response(400, {"error": "Email is required in the URL path."})

    try:
        table = dynamodb.Table(REGISTRATIONS_TABLE_NAME)
        result = table.query(
            IndexName=EMAIL_INDEX_NAME,
            KeyConditionExpression=Key("email").eq(email),
        )
        registrations = result.get("Items", [])

        logger.info(f"Found {len(registrations)} registrations for {email}")
        return build_response(
            200, {"registrations": registrations, "count": len(registrations)}
        )

    except Exception as e:
        logger.error(f"Error fetching registrations for {email}: {str(e)}")
        return build_response(
            500, {"error": "Failed to retrieve registrations. Please try again later."}
        )