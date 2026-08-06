/**
 * Renders a single event as an HTML string (a lightweight "component" —
 * just a pure function that takes data and returns markup).
 */

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function getSeatsLabel(event) {
  const remaining = event.capacity - event.registeredCount;
  if (remaining <= 0) return { text: "Fully booked", className: "badge--danger" };
  if (remaining <= 5) return { text: `${remaining} seats left`, className: "badge--warning" };
  return { text: `${remaining} seats left`, className: "badge--success" };
}

export function renderEventCard(event) {
  const seats = getSeatsLabel(event);
  const isFull = event.capacity - event.registeredCount <= 0;

  return `
    <article class="event-card" data-event-id="${event.eventId}">
      <div class="event-card__top">
        <span class="badge badge--category">${event.category || "General"}</span>
        <span class="badge ${seats.className}">${seats.text}</span>
      </div>
      <h3 class="event-card__title">${event.eventName}</h3>
      <p class="event-card__description">${event.description || ""}</p>
      <div class="event-card__meta">
        <span class="event-card__meta-item">📅 ${formatDate(event.eventDate)}</span>
        <span class="event-card__meta-item">📍 ${event.location || "TBA"}</span>
      </div>
      <button
        class="btn btn--primary btn--full register-btn"
        data-event-id="${event.eventId}"
        ${isFull ? "disabled" : ""}
      >
        ${isFull ? "Fully Booked" : "Register Now"}
      </button>
    </article>
  `;
}

export function renderEventCardSkeleton() {
  return `
    <div class="event-card event-card--skeleton">
      <div class="skeleton skeleton--badge"></div>
      <div class="skeleton skeleton--title"></div>
      <div class="skeleton skeleton--text"></div>
      <div class="skeleton skeleton--text" style="width: 60%"></div>
      <div class="skeleton skeleton--button"></div>
    </div>
  `;
}