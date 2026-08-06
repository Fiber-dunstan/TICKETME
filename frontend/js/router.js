/**
 * Lightweight hash-based router.
 * Maps a URL hash (e.g. "#/events") to a view-rendering function, and
 * re-renders #app-content whenever the hash changes — no page reloads.
 */

const routes = {};
let currentCleanup = null;

export function registerRoute(path, renderFn) {
  routes[path] = renderFn;
}

function getCurrentPath() {
  const hash = window.location.hash.replace("#", "");
  return hash || "/events";
}

async function renderCurrentRoute() {
  const path = getCurrentPath();
  const container = document.getElementById("app-content");

  // Run any cleanup the previous view registered (e.g. clearing intervals).
  if (typeof currentCleanup === "function") {
    currentCleanup();
    currentCleanup = null;
  }

  updateActiveNavLink(path);

  const renderFn = routes[path] || routes["/events"];
  container.innerHTML = "";
  currentCleanup = await renderFn(container);
}

function updateActiveNavLink(path) {
  document.querySelectorAll("[data-nav-link]").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.route === path);
  });
}

export function initRouter() {
  window.addEventListener("hashchange", renderCurrentRoute);
  window.addEventListener("DOMContentLoaded", renderCurrentRoute);
}