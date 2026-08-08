(function () {
  const toc = document.querySelector("[data-detail-toc]");
  const sections = Array.from(
    document.querySelectorAll(".detail-section[id]"),
  );
  if (!sections.length) return;

  const openIds = new Set(["identity"]);
  const hashId = (location.hash || "").replace(/^#/, "");
  if (hashId) openIds.add(hashId);

  function wrapBody(section) {
    if (section.querySelector(".detail-section-body")) return;
    const head = section.querySelector(".section-head");
    if (!head) return;
    const body = document.createElement("div");
    body.className = "detail-section-body";
    let node = head.nextSibling;
    while (node) {
      const next = node.nextSibling;
      body.appendChild(node);
      node = next;
    }
    section.appendChild(body);
  }

  function setOpen(section, open, focusToggle) {
    const body = section.querySelector(".detail-section-body");
    const toggle = section.querySelector("[data-detail-toggle]");
    if (!body || !toggle) return;
    section.classList.toggle("is-open", open);
    section.classList.toggle("is-collapsed", !open);
    body.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (focusToggle) toggle.focus({ preventScroll: true });
  }

  function syncToc() {
    if (!toc) return;
    toc.querySelectorAll("[data-toc-target]").forEach((link) => {
      const id = link.getAttribute("data-toc-target");
      const section = id && document.getElementById(id);
      const active = !!(section && section.classList.contains("is-open"));
      link.classList.toggle("is-active", active);
      link.setAttribute("aria-current", active ? "true" : "false");
    });
  }

  sections.forEach((section) => {
    wrapBody(section);
    const head = section.querySelector(".section-head");
    const body = section.querySelector(".detail-section-body");
    if (!head || !body) return;

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "detail-section-toggle";
    toggle.setAttribute("data-detail-toggle", "");
    toggle.setAttribute(
      "aria-controls",
      section.id + "-body",
    );
    body.id = section.id + "-body";

    while (head.firstChild) toggle.appendChild(head.firstChild);
    const chevron = document.createElement("span");
    chevron.className = "detail-section-chevron";
    chevron.setAttribute("aria-hidden", "true");
    toggle.appendChild(chevron);
    head.appendChild(toggle);

    const shouldOpen = openIds.has(section.id);
    setOpen(section, shouldOpen, false);

    toggle.addEventListener("click", () => {
      const open = !section.classList.contains("is-open");
      setOpen(section, open, false);
      syncToc();
      if (open && history.replaceState) {
        history.replaceState(null, "", "#" + section.id);
      }
    });
  });

  if (toc) {
    toc.querySelectorAll("a[href^='#']").forEach((link) => {
      const id = (link.getAttribute("href") || "").slice(1);
      if (id) link.setAttribute("data-toc-target", id);
      link.addEventListener("click", (e) => {
        const targetId = link.getAttribute("data-toc-target");
        const section = targetId && document.getElementById(targetId);
        if (!section) return;
        e.preventDefault();
        setOpen(section, true, false);
        syncToc();
        section.scrollIntoView({ behavior: "smooth", block: "start" });
        if (history.replaceState) {
          history.replaceState(null, "", "#" + targetId);
        }
      });
    });
  }

  syncToc();

  window.addEventListener("hashchange", () => {
    const id = (location.hash || "").replace(/^#/, "");
    const section = id && document.getElementById(id);
    if (!section) return;
    setOpen(section, true, false);
    syncToc();
    section.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
