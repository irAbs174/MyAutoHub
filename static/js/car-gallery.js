(function () {
  const root = document.querySelector("[data-car-gallery]");
  const dataEl = document.getElementById("car-gallery-data");
  if (!root || !dataEl) return;

  let images = [];
  try {
    images = JSON.parse(dataEl.textContent || "[]");
  } catch (_) {
    return;
  }
  if (!Array.isArray(images) || !images.length) return;

  const labels = {
    close: root.dataset.labelClose || "Close",
    prev: root.dataset.labelPrev || "Previous",
    next: root.dataset.labelNext || "Next",
    zoomIn: root.dataset.labelZoomIn || "Zoom in",
    zoomOut: root.dataset.labelZoomOut || "Zoom out",
  };

  let index = 0;
  let zoomed = false;
  let touchStartX = 0;
  let touchStartY = 0;
  let touchDeltaX = 0;
  let wheelLock = false;

  const overlay = document.createElement("div");
  overlay.className = "car-lightbox";
  overlay.hidden = true;
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Gallery");
  overlay.innerHTML = `
    <div class="car-lightbox-backdrop" data-lightbox-close></div>
    <div class="car-lightbox-frame">
      <button type="button" class="car-lightbox-close" data-lightbox-close aria-label="${labels.close}">×</button>
      <button type="button" class="car-lightbox-nav car-lightbox-prev" data-lightbox-prev aria-label="${labels.prev}">‹</button>
      <button type="button" class="car-lightbox-nav car-lightbox-next" data-lightbox-next aria-label="${labels.next}">›</button>
      <div class="car-lightbox-stage" data-lightbox-stage>
        <img class="car-lightbox-image" data-lightbox-image alt="" draggable="false">
      </div>
      <p class="car-lightbox-caption" data-lightbox-caption hidden></p>
      <p class="car-lightbox-counter" data-lightbox-counter></p>
    </div>
  `;
  document.body.appendChild(overlay);

  const imgEl = overlay.querySelector("[data-lightbox-image]");
  const stageEl = overlay.querySelector("[data-lightbox-stage]");
  const captionEl = overlay.querySelector("[data-lightbox-caption]");
  const counterEl = overlay.querySelector("[data-lightbox-counter]");
  const prevBtn = overlay.querySelector("[data-lightbox-prev]");
  const nextBtn = overlay.querySelector("[data-lightbox-next]");

  function syncThumbs() {
    root.querySelectorAll("[data-gallery-index]").forEach((btn) => {
      const i = Number(btn.dataset.galleryIndex);
      btn.classList.toggle("is-active", i === index && !btn.classList.contains("car-gallery-more"));
    });
  }

  function render() {
    const item = images[index];
    if (!item) return;
    imgEl.src = item.url;
    imgEl.alt = item.caption || "";
    if (item.caption) {
      captionEl.hidden = false;
      captionEl.textContent = item.caption;
    } else {
      captionEl.hidden = true;
      captionEl.textContent = "";
    }
    counterEl.textContent = `${index + 1} / ${images.length}`;
    setZoom(false);
    const multi = images.length > 1;
    prevBtn.hidden = !multi;
    nextBtn.hidden = !multi;
    syncThumbs();
  }

  function setZoom(on) {
    zoomed = !!on;
    stageEl.classList.toggle("is-zoomed", zoomed);
    imgEl.classList.toggle("is-zoomed", zoomed);
    imgEl.setAttribute("aria-label", zoomed ? labels.zoomOut : labels.zoomIn);
  }

  function open(at) {
    index = Math.max(0, Math.min(images.length - 1, Number(at) || 0));
    render();
    overlay.hidden = false;
    document.documentElement.classList.add("car-lightbox-open");
    overlay.focus?.();
  }

  function close() {
    overlay.hidden = true;
    document.documentElement.classList.remove("car-lightbox-open");
    setZoom(false);
  }

  function step(delta) {
    if (images.length < 2) return;
    index = (index + delta + images.length) % images.length;
    render();
  }

  root.querySelectorAll("[data-gallery-open]").forEach((btn) => {
    btn.addEventListener("click", () => {
      open(btn.dataset.galleryIndex || 0);
    });
  });

  overlay.querySelectorAll("[data-lightbox-close]").forEach((el) => {
    el.addEventListener("click", close);
  });
  prevBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    step(-1);
  });
  nextBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    step(1);
  });

  imgEl.addEventListener("click", (e) => {
    e.stopPropagation();
    setZoom(!zoomed);
  });

  stageEl.addEventListener(
    "wheel",
    (e) => {
      if (images.length < 2) return;
      e.preventDefault();
      if (wheelLock) return;
      wheelLock = true;
      step(e.deltaY > 0 || e.deltaX > 0 ? 1 : -1);
      window.setTimeout(() => {
        wheelLock = false;
      }, 280);
    },
    { passive: false },
  );

  stageEl.addEventListener(
    "touchstart",
    (e) => {
      if (!e.touches.length) return;
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      touchDeltaX = 0;
    },
    { passive: true },
  );

  stageEl.addEventListener(
    "touchmove",
    (e) => {
      if (!e.touches.length) return;
      touchDeltaX = e.touches[0].clientX - touchStartX;
      const dy = e.touches[0].clientY - touchStartY;
      if (Math.abs(touchDeltaX) > Math.abs(dy) && Math.abs(touchDeltaX) > 12) {
        e.preventDefault();
      }
    },
    { passive: false },
  );

  stageEl.addEventListener("touchend", () => {
    if (Math.abs(touchDeltaX) < 48) return;
    step(touchDeltaX < 0 ? 1 : -1);
    touchDeltaX = 0;
  });

  document.addEventListener("keydown", (e) => {
    if (overlay.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
    if (e.key === " " || e.key === "Enter") {
      if (e.target === imgEl || e.target === stageEl) {
        e.preventDefault();
        setZoom(!zoomed);
      }
    }
  });
})();
