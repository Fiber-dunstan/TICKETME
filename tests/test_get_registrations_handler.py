"""
Unit tests for the get_registrations Lambda handler.
"""
import os
import sys
import importlib.util
import boto3
from moto import mock_aws

SHARED_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "lambda", "shared")
HANDLER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "lambda", "get_registrations_handler", "app.py"
)

sys.path.append(SHARED_DIR)

os.environ["REGISTRATIONS_TABLE"] = "ticketme-registrations"
os.environ["EMAIL_INDEX_NAME"] = "email-index"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def _load_handler_module():
    spec = importlib.util.spec_from_file_location("get_registrations_app", HANDLER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _setup_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
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
    return table


@mock_aws
def test_returns_registrations_for_email():
    table = _setup_table()
    table.put_item(Item={
        "registrationId": "reg-1", "email": "jane@example.com",
        "eventId": "evt-1", "status": "CONFIRMED",
    })
    table.put_item(Item={
        "registrationId": "reg-2", "email": "other@example.com",
        "eventId": "evt-1", "status": "CONFIRMED",
    })
    app = _load_handler_module()

    response = app.handler({"pathParameters": {"email": "jane@example.com"}}, {})

    assert response["statusCode"] == 200
    assert "reg-1" in response["body"]
    assert "reg-2" not in response["body"]


@mock_aws
def test_returns_empty_list_for_unknown_email():
    _setup_table()
    app = _load_handler_module()

    response = app.handler({"pathParameters": {"email": "nobody@example.com"}}, {})

    assert response["statusCode"] == 200
    assert '"count": 0' in response["body"]


@mock_aws
def test_missing_email_returns_400():
    _setup_table()
    app = _load_handler_module()

    response = app.handler({"pathParameters": {}}, {})

    assert response["statusCode"] == 400