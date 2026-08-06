TicketMe Data Model
Overview
TicketMe uses two Amazon DynamoDB tables designed around the application's access patterns. The schema follows DynamoDB best practices by optimizing for query efficiency rather than relational database normalization.
________________________________________
Table: ticketme-events
This table stores information about all events available in the application.
Attribute	Data Type	Key	Description
eventId	String (UUID)	Partition Key	Unique identifier for an event
eventName	String		Name of the event
description	String		Event description
category	String		Event category
eventDate	String (ISO 8601)		Date and time of the event
location	String		Event venue
capacity	Number		Maximum number of attendees
registeredCount	Number		Current number of registered attendees
createdAt	String (ISO 8601)		Timestamp when the event was created
________________________________________
Table: ticketme-registrations
This table stores user registrations for events.
Attribute	Data Type	Key	Description
registrationId	String (UUID)	Partition Key	Unique identifier for a registration
eventId	String		Identifier of the associated event
email	String		Registrant's email address
fullName	String		Registrant's full name
phone       string      registers contact or phone number
status	String		Registration status (CONFIRMED or CANCELLED)
registeredAt	String (ISO 8601)		Registration timestamp
ticketCode	String		Unique ticket reference
________________________________________
Global Secondary Index
Index Name: email-index
Property	Value
Partition Key	email
Purpose	Retrieves all registrations associated with a specific email address without scanning the entire table.
________________________________________
Supported Access Patterns
Application Operation	DynamoDB Operation
List all events	Scan ticketme-events
Create a new event registration	PutItem into ticketme-registrations
Retrieve all registrations for a user	Query email-index
Cancel a registration	DeleteItem using registrationId
Check event capacity	Read registeredCount from the corresponding event
________________________________________
Design Decisions
The database uses two separate tables to maintain a simple and maintainable structure appropriate for the project's scope.
The registeredCount attribute is stored within each event record to enable efficient capacity checks without counting registration records.
A Global Secondary Index on the email attribute allows the application to retrieve all registrations for a user efficiently while avoiding full table scans.
This design provides efficient read and write operations for the application's primary workflows while remaining scalable and aligned with DynamoDB best practices.

