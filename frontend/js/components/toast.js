/**
 * Toast notification component.
 * Renders a temporary, auto-dismissing message into #toast-container.
 * Used for success/error feedback after actions like register/cancel.
 */

export function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");

  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `
    <span class="toast__icon">${type === "success" ? "✓" : "⚠"}</span>
    <span class="toast__message">${message}</span>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add("toast--visible"));

  setTimeout(() => {
    toast.classList.remove("toast--visible");
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}