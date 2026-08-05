"""
Shared utility for building consistent, CORS-enabled API Gateway responses
across all TicketMe Lambda functions.
"""
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """
    DynamoDB returns numeric values as Python Decimal objects, which the
    standard json library cannot serialize by default. This encoder converts
    them to plain int/float so json.dumps() doesn't crash.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)


def build_response(status_code: int, body: dict) -> dict:
    """
    Builds a standardized API Gateway Lambda proxy response.

    Args:
        status_code: HTTP status code (200, 400, 404, 500, etc.)
        body: A JSON-serializable dictionary to return to the client.

    Returns:
        A dict in the exact shape API Gateway requires.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,DELETE",
        },
        "body": json.dumps(body, cls=DecimalEncoder),
    }