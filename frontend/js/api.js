/**
 * TicketMe API Client
 * Centralizes every call to the backend REST API. No other file in the
 * frontend should call fetch() directly — this keeps the API contract in
 * exactly one place, so if an endpoint changes, we update it here only.
 */

// TODO: replace with your real API Gateway base URL from Terraform's output.
const API_BASE_URL = "https://isgeadr1n4.execute-api.us-east-1.amazonaws.com/dev";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Internal helper: performs a fetch call, parses JSON, and throws a
 * consistent ApiError on any failure so calling code doesn't need to
 * repeat try/catch response-checking logic everywhere.
 */
async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (networkError) {
    throw new ApiError("Network error — please check your connection.", 0);
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Response had no JSON body — fine for some responses.
  }

  if (!response.ok) {
    const message = data?.error || `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status);
  }

  return data;
}

export const api = {
  listEvents() {
    return request("/events", { method: "GET" });
  },

  register({ email, fullName, phoneNumber, eventId }) {
    return request("/register", {
      method: "POST",
      body: JSON.stringify({ email, fullName, phoneNumber, eventId }),
    });
  },

  getRegistrationsByEmail(email) {
    return request(`/registrations/${encodeURIComponent(email)}`, { method: "GET" });
  },

  cancelRegistration(registrationId) {
    return request(`/registration/${encodeURIComponent(registrationId)}`, { method: "DELETE" });
  },
};

export { ApiError };