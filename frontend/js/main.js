/**
 * App entry point: registers routes and starts the router.
 */
import { initRouter, registerRoute } from "./router.js";
import { renderEventsView } from "./views/eventsView.js";
import { renderRegistrationsView } from "./views/registrationsView.js";

registerRoute("/events", renderEventsView);
registerRoute("/my-registrations", renderRegistrationsView);
// "/my-registrations" route added in the next step.

initRouter();

// Dark/light theme toggle
const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");
const savedTheme = localStorage.getItem("ticketme_theme") || "dark";

if (savedTheme === "light") {
  document.body.classList.add("theme-light");
  themeIcon.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {
  const isLight = document.body.classList.toggle("theme-light");
  themeIcon.textContent = isLight ? "☀️" : "🌙";
  localStorage.setItem("ticketme_theme", isLight ? "light" : "dark");
});
