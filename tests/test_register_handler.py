"""
Unit tests for the register Lambda handler.
Covers: success, validation errors, missing event, duplicate registration,
and full-capacity rejection — all using moto (no real AWS calls).
"""
import os
import sys
import json
import importlib.util
import boto3
from moto import mock_aws

SHARED_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "shared")
HANDLER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "lambda", "register_handler", "app.py"
)

sys.path.append(SHARED_DIR)

os.environ["EVENTS_TABLE"] = "ticketme-events"
os.environ["REGISTRATIONS_TABLE"] = "ticketme-registrations"
os.environ["EMAIL_INDEX_NAME"] = "email-index"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def _load_handler_module():
    """
    Loads register_handler/app.py by its explicit file path under a unique
    module name ('register_app'), avoiding collisions with other Lambda
    handlers that are also named app.py.
    """
    spec = importlib.util.spec_from_file_location("register_app", HANDLER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _setup_tables():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    events_table = dynamodb.create_table(
        TableName="ticketme-events",
        KeySchema=[{"AttributeName": "eventId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "eventId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    registrations_table = dynamodb.create_table(
        TableName="ticketme-registrations",
        KeySchema=[{"AttributeName": "registrationId", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "registrationId", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-index",
                "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    return events_table, registrations_table


def _valid_body(event_id="evt-1"):
    return json.dumps({
        "email": "jane@example.com",
        "fullName": "Jane Doe",
        "phoneNumber": "+233555123456",
        "eventId": event_id,
    })


@mock_aws
def test_successful_registration():
    events_table, _ = _setup_tables()
    events_table.put_item(Item={"eventId": "evt-1", "eventName": "AWS Summit", "capacity": 10, "registeredCount": 0})
    app = _load_handler_module()

    response = app.handler({"body": _valid_body()}, {})
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["registration"]["email"] == "jane@example.com"
    assert "ticketCode" in body["registration"]


@mock_aws
def test_missing_fields_returns_400():
    _setup_tables()
    app = _load_handler_module()

    response = app.handler({"body": json.dumps({"email": "bad"})}, {})
    assert response["statusCode"] == 400


@mock_aws
def test_event_not_found_returns_404():
    _setup_tables()
    app = _load_handler_module()

    response = app.handler({"body": _valid_body(event_id="does-not-exist")}, {})
    assert response["statusCode"] == 404


@mock_aws
def test_duplicate_registration_returns_409():
    events_table, registrations_table = _setup_tables()
    events_table.put_item(Item={"eventId": "evt-1", "eventName": "AWS Summit", "capacity": 10, "registeredCount": 1})
    registrations_table.put_item(Item={
        "registrationId": "reg-1",
        "eventId": "evt-1",
        "email": "jane@example.com",
        "fullName": "Jane Doe",
        "phoneNumber": "+233555123456",
        "status": "CONFIRMED",
        "registeredAt": "2026-01-01T00:00:00+00:00",
        "ticketCode": "ABC12345",
    })
    app = _load_handler_module()

    response = app.handler({"body": _valid_body()}, {})
    assert response["statusCode"] == 409


@mock_aws
def test_event_full_returns_409():
    events_table, _ = _setup_tables()
    events_table.put_item(Item={"eventId": "evt-1", "eventName": "AWS Summit", "capacity": 1, "registeredCount": 1})
    app = _load_handler_module()

    response = app.handler({"body": _valid_body()}, {})
    assert response["statusCode"] == 409