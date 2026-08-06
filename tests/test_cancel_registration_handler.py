"""
Unit tests for the cancel_registration Lambda handler.
"""
import os
import sys
import importlib.util
import boto3
from moto import mock_aws

SHARED_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "shared")
HANDLER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "lambda", "cancel_registration_handler", "app.py"
)

sys.path.append(SHARED_DIR)

os.environ["EVENTS_TABLE"] = "ticketme-events"
os.environ["REGISTRATIONS_TABLE"] = "ticketme-registrations"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def _load_handler_module():
    spec = importlib.util.spec_from_file_location("cancel_registration_app", HANDLER_PATH)
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
        AttributeDefinitions=[{"AttributeName": "registrationId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    return events_table, registrations_table


@mock_aws
def test_successful_cancellation():
    events_table, registrations_table = _setup_tables()
    events_table.put_item(Item={"eventId": "evt-1", "capacity": 10, "registeredCount": 5})
    registrations_table.put_item(Item={
        "registrationId": "reg-1", "eventId": "evt-1",
        "email": "jane@example.com", "status": "CONFIRMED",
    })
    app = _load_handler_module()

    response = app.handler({"pathParameters": {"id": "reg-1"}}, {})

    assert response["statusCode"] == 200
    updated = registrations_table.get_item(Key={"registrationId": "reg-1"})["Item"]
    assert updated["status"] == "CANCELLED"
    updated_event = events_table.get_item(Key={"eventId": "evt-1"})["Item"]
    assert updated_event["registeredCount"] == 4


@mock_aws
def test_cancel_nonexistent_registration_returns_404():
    _setup_tables()
    app = _load_handler_module()

    response = app.handler({"pathParameters": {"id": "does-not-exist"}}, {})

    assert response["statusCode"] == 404


@mock_aws
def test_cancel_already_cancelled_returns_409():
    events_table, registrations_table = _setup_tables()
    events_table.put_item(Item={"eventId": "evt-1", "capacity": 10, "registeredCount": 5})
    registrations_table.put_item(Item={
        "registrationId": "reg-1", "eventId": "evt-1",
        "email": "jane@example.com", "status": "CANCELLED",
    })
    app = _load_handler_module()

    response = app.handler({"pathParameters": {"id": "reg-1"}}, {})

    assert response["statusCode"] == 409


@mock_aws
def test_missing_id_returns_400():
    _setup_tables()
    app = _load_handler_module()

    response = app.handler({"pathParameters": {}}, {})

    assert response["statusCode"] == 400