"""
Unit tests for the list_events Lambda handler.
Uses moto to simulate DynamoDB in memory — no real AWS calls, no cost.
"""
import os
import sys
import importlib.util
import boto3
from moto import mock_aws

SHARED_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "shared")
HANDLER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "lambda", "list_events_handler", "app.py"
)

sys.path.append(SHARED_DIR)

os.environ["EVENTS_TABLE"] = "ticketme-events"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def _load_handler_module():
    """
    Loads list_events_handler/app.py by its explicit file path under a unique
    module name ('list_events_app'), avoiding collisions with other Lambda
    handlers that are also named app.py.
    """
    spec = importlib.util.spec_from_file_location("list_events_app", HANDLER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _create_fake_events_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="ticketme-events",
        KeySchema=[{"AttributeName": "eventId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "eventId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    return table


@mock_aws
def test_list_events_returns_empty_list_when_table_is_empty():
    _create_fake_events_table()
    app = _load_handler_module()

    response = app.handler({}, {})

    assert response["statusCode"] == 200
    assert '"count": 0' in response["body"]


@mock_aws
def test_list_events_returns_seeded_events():
    table = _create_fake_events_table()
    table.put_item(Item={"eventId": "evt-1", "eventName": "AWS Summit"})
    app = _load_handler_module()

    response = app.handler({}, {})

    assert response["statusCode"] == 200
    assert "AWS Summit" in response["body"]