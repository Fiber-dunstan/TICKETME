"""
TicketMe - List Events Lambda
Handles: GET /events
Returns all events currently stored in the ticketme-events DynamoDB table.
"""
import os
import sys
import boto3

# Allow this function to import shared/ utilities both locally and when
# packaged for deployment (build script copies shared/ alongside each function).
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "shared"))

from response_utils import build_response  # noqa: E402
from logger import get_logger  # noqa: E402

logger = get_logger(__name__)

dynamodb = boto3.resource("dynamodb")
EVENTS_TABLE_NAME = os.environ.get("EVENTS_TABLE", "ticketme-events")


def handler(event, context):
    logger.info("Received request to list events")

    try:
        table = dynamodb.Table(EVENTS_TABLE_NAME)
        result = table.scan()
        events = result.get("Items", [])

        logger.info(f"Retrieved {len(events)} events")
        return build_response(200, {"events": events, "count": len(events)})

    except Exception as e:
        logger.error(f"Error listing events: {str(e)}")
        return build_response(
            500, {"error": "Failed to retrieve events. Please try again later."}
        )