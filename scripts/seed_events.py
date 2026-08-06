"""
One-off script to seed sample events into the ticketme-dev-events DynamoDB
table for manual testing. Run with: python scripts/seed_events.py
"""
import uuid
from datetime import datetime, timedelta, timezone
import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("ticketme-dev-events")

sample_events = [
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "AWS Cloud Summit 2026",
        "description": "A full-day summit on modern cloud architecture and serverless patterns.",
        "category": "Tech",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        "location": "Accra International Conference Centre",
        "capacity": 100,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "Startup Founders Networking Night",
        "description": "An evening of networking for early-stage founders and investors.",
        "category": "Networking",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
        "location": "Kumasi Tech Hub",
        "capacity": 50,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
]

for event in sample_events:
    table.put_item(Item=event)
    print(f"Seeded: {event['eventName']} ({event['eventId']})")

print("Done.")