/**
 * Minimal in-memory application state.
 * Not a full state-management library — just a single shared object plus
 * a tiny pub/sub mechanism, enough for an app this size without adding a
 * framework dependency.
 */

const state = {
  events: [],
  registeredEmail: localStorage.getItem("ticketme_email") || "",
};

const listeners = new Set();

export function getState() {
  return state;
}

export function setState(patch) {
  Object.assign(state, patch);
  listeners.forEach((listener) => listener(state));
}

export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function rememberEmail(email) {
  state.registeredEmail = email;
  localStorage.setItem("ticketme_email", email);
}