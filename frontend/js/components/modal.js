/**
 * A generic, reusable modal dialog. Renders an overlay + panel into the
 * document body, and returns a controller object to close it programmatically.
 */

export function openModal({ title, bodyHtml, onMount }) {
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-label="${title}">
      <div class="modal__header">
        <h2 class="modal__title">${title}</h2>
        <button class="icon-button modal__close" aria-label="Close">✕</button>
      </div>
      <div class="modal__body">${bodyHtml}</div>
    </div>
  `;

  document.body.appendChild(overlay);
  document.body.style.overflow = "hidden";
  requestAnimationFrame(() => overlay.classList.add("modal-overlay--visible"));

  function close() {
    overlay.classList.remove("modal-overlay--visible");
    document.body.style.overflow = "";
    setTimeout(() => overlay.remove(), 200);
  }

  overlay.querySelector(".modal__close").addEventListener("click", close);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });

  if (typeof onMount === "function") {
    onMount(overlay, close);
  }

  return { close, overlay };
}