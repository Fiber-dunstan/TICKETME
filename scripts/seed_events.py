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
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "Men in Tech Breakfast",
        "description": "A morning of talks and networking celebrating men building in tech across Ghana.",
        "category": "Networking",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=21)).isoformat(),
        "location": "Kempinski Hotel, Accra",
        "capacity": 80,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "DevOps & Cloud Bootcamp",
        "description": "A hands-on weekend workshop covering CI/CD, containers, and infrastructure as code.",
        "category": "Tech",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=45)).isoformat(),
        "location": "Virtual",
        "capacity": 150,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "Forex Trading Masterclass",
        "description": "A full-day intensive on UX research, prototyping, and design systems.",
        "category": "Design",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "location": "Impact Hub Accra",
        "capacity": 40,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
    {
        "eventId": str(uuid.uuid4()),
        "eventName": "Startup Pitch Night",
        "description": "Early-stage founders pitch to a panel of investors and the local startup community.",
        "category": "Business",
        "eventDate": (datetime.now(timezone.utc) + timedelta(days=60)).isoformat(),
        "location": "Mestem Hub, Kumasi",
        "capacity": 120,
        "registeredCount": 0,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    },
]

for event in sample_events:
    table.put_item(Item=event)
    print(f"Seeded: {event['eventName']} ({event['eventId']})")

print("Done.")