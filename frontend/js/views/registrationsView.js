/**
 * My Registrations view: lets a user look up their registrations by email,
 * view ticket details, and cancel a registration.
 */
import { api, ApiError } from "../api.js";
import { getState, rememberEmail } from "../state.js";
import { showToast } from "../components/toast.js";

export async function renderRegistrationsView(container) {
  const { registeredEmail } = getState();

  container.innerHTML = `
    <div class="view-header">
      <div>
        <h1 class="view-title">My Registrations</h1>
        <p class="view-subtitle">Look up your tickets using the email you registered with.</p>
      </div>
    </div>

    <div class="toolbar">
      <input
        type="email"
        id="lookup-email"
        class="input"
        placeholder="you@example.com"
        value="${registeredEmail}"
      />
      <button id="lookup-btn" class="btn btn--primary">Find My Registrations</button>
    </div>

    <div id="registrations-list" class="registrations-list"></div>
  `;

  const emailInput = container.querySelector("#lookup-email");
  const lookupBtn = container.querySelector("#lookup-btn");
  const listEl = container.querySelector("#registrations-list");

  async function lookup() {
    const email = emailInput.value.trim().toLowerCase();
    if (!email) {
      showToast("Please enter an email address.", "error");
      return;
    }

    rememberEmail(email);
    listEl.innerHTML = renderLoadingState();
    lookupBtn.disabled = true;

    try {
      const data = await api.getRegistrationsByEmail(email);
      renderRegistrations(data.registrations || []);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Failed to load registrations.";
      listEl.innerHTML = renderErrorState(message);
    } finally {
      lookupBtn.disabled = false;
    }
  }

  function renderRegistrations(registrations) {
    if (registrations.length === 0) {
      listEl.innerHTML = renderEmptyState();
      return;
    }

    listEl.innerHTML = registrations.map(renderRegistrationCard).join("");
  }

  listEl.addEventListener("click", async (e) => {
    const cancelBtn = e.target.closest(".cancel-btn");
    if (!cancelBtn) return;

    const registrationId = cancelBtn.dataset.registrationId;
    const confirmed = confirm("Cancel this registration? This can't be undone.");
    if (!confirmed) return;

    cancelBtn.disabled = true;
    cancelBtn.textContent = "Cancelling...";

    try {
      await api.cancelRegistration(registrationId);
      showToast("Registration cancelled.", "success");
      lookup(); // refresh the list
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Failed to cancel registration.";
      showToast(message, "error");
      cancelBtn.disabled = false;
      cancelBtn.textContent = "Cancel Registration";
    }
  });

  lookupBtn.addEventListener("click", lookup);
  emailInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") lookup();
  });

  // Auto-lookup if we already remember an email from a previous visit.
  if (registeredEmail) {
    lookup();
  }
}

function renderRegistrationCard(reg) {
  const isCancelled = reg.status === "CANCELLED";
  return `
    <div class="reg-card ${isCancelled ? "reg-card--cancelled" : ""}">
      <div class="reg-card__info">
        <div class="reg-card__ticket-code">${reg.ticketCode}</div>
        <div class="reg-card__event-id">Event ID: ${reg.eventId}</div>
        <span class="badge ${isCancelled ? "badge--danger" : "badge--success"}">
          ${isCancelled ? "Cancelled" : "Confirmed"}
        </span>
      </div>
      ${
        !isCancelled
          ? `<button class="btn btn--danger cancel-btn" data-registration-id="${reg.registrationId}">Cancel Registration</button>`
          : ""
      }
    </div>
  `;
}

function renderLoadingState() {
  return `<div class="empty-state">Searching...</div>`;
}

function renderEmptyState() {
  return `
    <div class="empty-state">
      <div class="empty-state__icon">🎫</div>
      <h3>No registrations found</h3>
      <p>Register for an event first, then check back here.</p>
    </div>
  `;
}

function renderErrorState(message) {
  return `
    <div class="empty-state empty-state--error">
      <div class="empty-state__icon">⚠</div>
      <h3>Something went wrong</h3>
      <p>${message}</p>
    </div>
  `;
}