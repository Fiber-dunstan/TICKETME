"""
Shared input validation for TicketMe Lambda functions.
"""
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-()]{7,15}$")


def validate_registration_input(data: dict):
    """
    Validates raw registration input.

    Returns:
        (errors, cleaned_data) — errors is a list of human-readable strings
        (empty if valid). cleaned_data has whitespace-trimmed, normalized values.
    """
    errors = []

    email = (data.get("email") or "").strip().lower()
    full_name = (data.get("fullName") or "").strip()
    phone = (data.get("phoneNumber") or "").strip()
    event_id = (data.get("eventId") or "").strip()

    if not email or not EMAIL_REGEX.match(email):
        errors.append("A valid email address is required.")

    if not full_name or len(full_name) < 2:
        errors.append("Full name is required (minimum 2 characters).")

    if not phone or not PHONE_REGEX.match(phone):
        errors.append("A valid phone number is required.")

    if not event_id:
        errors.append("eventId is required.")

    cleaned_data = {
        "email": email,
        "fullName": full_name,
        "phoneNumber": phone,
        "eventId": event_id,
    }

    return errors, cleaned_data