(function () {
  document.querySelectorAll("[data-catalog-card]").forEach((card) => {
    const toggle = card.querySelector("[data-catalog-toggle]");
    const panel = card.querySelector("[data-catalog-panel]");
    if (!toggle || !panel) return;

    const setOpen = (open) => {
      card.classList.toggle("is-open", open);
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    };

    setOpen(false);

    toggle.addEventListener("click", () => {
      setOpen(!card.classList.contains("is-open"));
    });

    toggle.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setOpen(!card.classList.contains("is-open"));
      }
    });
  });
})();
