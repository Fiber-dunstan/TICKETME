/**
 * Events view: fetches and renders the live events list, with search,
 * category filtering, loading/empty/error states, and the registration flow.
 */
import { api, ApiError } from "../api.js";
import { getState, setState, rememberEmail } from "../state.js";
import { renderEventCard, renderEventCardSkeleton } from "../components/eventCard.js";
import { openModal } from "../components/modal.js";
import { showToast } from "../components/toast.js";

export async function renderEventsView(container) {
  container.innerHTML = `
    <div class="view-header">
      <div>
        <h1 class="view-title">Discover Events</h1>
        <p class="view-subtitle">Browse and register for upcoming events in seconds.</p>
      </div>
    </div>

    <div class="toolbar">
      <input
        type="search"
        id="event-search"
        class="input"
        placeholder="Search events by name..."
      />
      <select id="category-filter" class="select">
        <option value="">All categories</option>
      </select>
    </div>

    <div id="events-grid" class="events-grid">
      ${Array(6).fill(renderEventCardSkeleton()).join("")}
    </div>
  `;

  const grid = container.querySelector("#events-grid");
  const searchInput = container.querySelector("#event-search");
  const categoryFilter = container.querySelector("#category-filter");

  let allEvents = [];

  try {
    const data = await api.listEvents();
    allEvents = data.events || [];
    setState({ events: allEvents });
    populateCategoryFilter(categoryFilter, allEvents);
    renderList(allEvents);
  } catch (err) {
    renderError(grid, err);
    return;
  }

  function renderList(events) {
    if (events.length === 0) {
      grid.innerHTML = renderEmptyState();
      return;
    }
    grid.innerHTML = events.map(renderEventCard).join("");
  }

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    const category = categoryFilter.value;

    const filtered = allEvents.filter((event) => {
      const matchesQuery = event.eventName.toLowerCase().includes(query);
      const matchesCategory = !category || event.category === category;
      return matchesQuery && matchesCategory;
    });

    renderList(filtered);
  }

  searchInput.addEventListener("input", debounce(applyFilters, 200));
  categoryFilter.addEventListener("change", applyFilters);

  // Event delegation: one listener handles clicks on any "Register" button,
  // including ones rendered after search/filter changes.
  grid.addEventListener("click", (e) => {
    const btn = e.target.closest(".register-btn");
    if (!btn) return;
    const event = allEvents.find((e) => e.eventId === btn.dataset.eventId);
    if (event) openRegistrationModal(event);
  });
}

function openRegistrationModal(event) {
  const { registeredEmail } = getState();

  const { close } = openModal({
    title: `Register for ${event.eventName}`,
    bodyHtml: `
      <form id="register-form" class="form">
        <label class="form-label">Full Name</label>
        <input type="text" name="fullName" class="input" required placeholder="Jane Doe" />

        <label class="form-label">Email</label>
        <input type="email" name="email" class="input" required placeholder="jane@example.com" value="${registeredEmail}" />

        <label class="form-label">Phone Number</label>
        <input type="tel" name="phoneNumber" class="input" required placeholder="+233 555 000 111" />

        <button type="submit" class="btn btn--primary btn--full" id="submit-btn">
          Confirm Registration
        </button>
      </form>
    `,
    onMount: (overlay) => {
      const form = overlay.querySelector("#register-form");
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector("#submit-btn");
        const formData = new FormData(form);

        submitBtn.disabled = true;
        submitBtn.textContent = "Registering...";

        try {
          const result = await api.register({
            email: formData.get("email"),
            fullName: formData.get("fullName"),
            phoneNumber: formData.get("phoneNumber"),
            eventId: event.eventId,
          });

          rememberEmail(formData.get("email").trim().toLowerCase());
          close();
          showToast(`You're registered! Ticket code: ${result.registration.ticketCode}`, "success");
          window.location.hash = "#/my-registrations";
        } catch (err) {
          const message = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
          showToast(message, "error");
          submitBtn.disabled = false;
          submitBtn.textContent = "Confirm Registration";
        }
      });
    },
  });
}

function populateCategoryFilter(select, events) {
  const categories = [...new Set(events.map((e) => e.category).filter(Boolean))];
  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    select.appendChild(option);
  });
}

function renderEmptyState() {
  return `
    <div class="empty-state">
      <div class="empty-state__icon">🔍</div>
      <h3>No events found</h3>
      <p>Try a different search term or check back later.</p>
    </div>
  `;
}

function renderError(grid, err) {
  const message = err instanceof ApiError ? err.message : "Failed to load events.";
  grid.innerHTML = `
    <div class="empty-state empty-state--error">
      <div class="empty-state__icon">⚠</div>
      <h3>Couldn't load events</h3>
      <p>${message}</p>
    </div>
  `;
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}