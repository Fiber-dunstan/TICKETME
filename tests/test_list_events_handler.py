"""
Unit tests for the list_events Lambda handler.
Uses moto to simulate DynamoDB in memory — no real AWS calls, no cost.
"""
import os
import sys
import importlib
import boto3
from moto import mock_aws

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "list_events_handler")
)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "shared"))

os.environ["EVENTS_TABLE"] = "ticketme-events"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@mock_aws
def test_list_events_returns_empty_list_when_table_is_empty():
    _create_fake_events_table()

    import app
    importlib.reload(app)  # re-import so it connects to our mocked DynamoDB

    response = app.handler({}, {})

    assert response["statusCode"] == 200
    assert '"count": 0' in response["body"]


@mock_aws
def test_list_events_returns_seeded_events():
    table = _create_fake_events_table()
    table.put_item(Item={"eventId": "evt-1", "eventName": "AWS Summit"})

    import app
    importlib.reload(app)

    response = app.handler({}, {})

    assert response["statusCode"] == 200
    assert "AWS Summit" in response["body"]


def _create_fake_events_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="ticketme-events",
        KeySchema=[{"AttributeName": "eventId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "eventId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    return table