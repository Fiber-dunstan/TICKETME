# TicketMe API Reference

Base URL: `https://isgeadr1n4.execute-api.us-east-1.amazonaws.com/dev`

All responses are JSON. All endpoints support CORS for browser-based clients.

---

## `GET /events`

Returns all available events.

**Request:** No parameters.

**Response `200 OK`:**
```json
{
  "events": [
    {
      "eventId": "dbada6ba-6f25-4dda-9002-203a6c2d4f01",
      "eventName": "AWS Cloud Summit 2026",
      "description": "A full-day summit on modern cloud architecture.",
      "category": "Tech",
      "eventDate": "2026-09-15T09:00:00Z",
      "location": "Accra International Conference Centre",
      "capacity": 100,
      "registeredCount": 12,
      "createdAt": "2026-08-01T10:00:00Z"
    }
  ],
  "count": 1
}
```

**Errors:** `500` — internal failure retrieving events.

---

## `POST /register`

Registers an attendee for an event.

**Request body:**
```json
{
  "email": "jane@example.com",
  "fullName": "Jane Doe",
  "phoneNumber": "+233555000111",
  "eventId": "dbada6ba-6f25-4dda-9002-203a6c2d4f01"
}
```

**Response `201 Created`:**
```json
{
  "message": "Registration successful",
  "registration": {
    "registrationId": "620b803f-3085-49e0-a51a-1c8b1056477f",
    "eventId": "dbada6ba-6f25-4dda-9002-203a6c2d4f01",
    "email": "jane@example.com",
    "fullName": "Jane Doe",
    "phoneNumber": "+233555000111",
    "status": "CONFIRMED",
    "registeredAt": "2026-08-06T08:36:15.445415+00:00",
    "ticketCode": "264C3A75"
  }
}
```

**Errors:**
| Status | Cause |
|---|---|
| `400` | Missing/invalid `email`, `fullName`, `phoneNumber`, or `eventId` |
| `404` | `eventId` does not exist |
| `409` | Already registered for this event, or event is at capacity |
| `500` | Internal failure |

---

## `GET /registrations/{email}`

Returns all registrations (any status) for the given email.

**Path parameter:** `email` — URL-encoded email address.

**Response `200 OK`:**
```json
{
  "registrations": [
    {
      "registrationId": "620b803f-3085-49e0-a51a-1c8b1056477f",
      "eventId": "dbada6ba-6f25-4dda-9002-203a6c2d4f01",
      "email": "jane@example.com",
      "fullName": "Jane Doe",
      "phoneNumber": "+233555000111",
      "status": "CONFIRMED",
      "registeredAt": "2026-08-06T08:36:15.445415+00:00",
      "ticketCode": "264C3A75"
    }
  ],
  "count": 1
}
```

An email with no registrations returns `200` with an empty array — this is not an error condition.

**Errors:** `400` — missing email in path. `500` — internal failure.

---

## `DELETE /registration/{id}`

Cancels a registration (soft delete — status set to `CANCELLED`, record retained for audit purposes). Frees the associated event's seat.

**Path parameter:** `id` — the `registrationId`.

**Response `200 OK`:**
```json
{ "message": "Registration cancelled successfully." }
```

**Errors:**
| Status | Cause |
|---|---|
| `400` | Missing registration id in path |
| `404` | Registration not found |
| `409` | Already cancelled |
| `500` | Internal failure |

---

## Error Response Shape

All error responses follow this shape:
```json
{ "error": "Human-readable message" }
```
Validation errors additionally include a `details` array:
```json
{ "error": "Validation failed", "details": ["A valid email address is required."] }
```