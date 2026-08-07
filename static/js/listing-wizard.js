(function () {
  function initListingWizard(root) {
    const panes = Array.from(root.querySelectorAll("[data-wizard-step]"));
    const indicators = Array.from(root.querySelectorAll("[data-step-indicator]"));
    const progress = root.querySelector("[data-wizard-progress]");
    const prevBtn = root.querySelector("[data-wizard-prev]");
    const nextBtn = root.querySelector("[data-wizard-next]");
    const submitBtn = root.querySelector("[data-wizard-submit]");
    const form = root.querySelector("form");
    if (!panes.length || !form || !nextBtn || !submitBtn) return;

    const total = panes.length;
    let step = 1;

    const firstErrorStep = () => {
      for (const pane of panes) {
        if (pane.querySelector(".form-error, .has-error")) {
          return Number(pane.dataset.wizardStep) || 1;
        }
      }
      return 1;
    };

    const showStep = (next) => {
      step = Math.min(Math.max(next, 1), total);
      panes.forEach((pane) => {
        const n = Number(pane.dataset.wizardStep);
        const active = n === step;
        pane.hidden = !active;
        pane.classList.toggle("is-active", active);
        if (active) {
          pane.classList.remove("is-enter");
          // Force reflow so enter animation restarts
          void pane.offsetWidth;
          pane.classList.add("is-enter");
        }
      });

      indicators.forEach((item) => {
        const n = Number(item.dataset.stepIndicator);
        item.classList.toggle("is-active", n === step);
        item.classList.toggle("is-done", n < step);
        item.setAttribute("aria-current", n === step ? "step" : "false");
      });

      if (progress) {
        const pct = total <= 1 ? 100 : ((step - 1) / (total - 1)) * 100;
        progress.style.width = pct + "%";
      }

      if (prevBtn) prevBtn.hidden = step <= 1;
      nextBtn.hidden = step >= total;
      submitBtn.hidden = step < total;

      const activePane = panes.find((p) => Number(p.dataset.wizardStep) === step);
      const focusable = activePane?.querySelector(
        "input:not([type='hidden']):not([type='file']), textarea, select",
      );
      if (focusable && !root.dataset.hasErrors) {
        window.setTimeout(() => focusable.focus({ preventScroll: true }), 180);
      }
    };

    const validateLangPair = (pane) => {
      const langs = ["fa", "en", "ar"];
      let complete = null;
      langs.forEach((code) => {
        const title = form.elements.namedItem(`title_${code}`);
        const description = form.elements.namedItem(`description_${code}`);
        const titleOk = title && typeof title.value === "string" && title.value.trim();
        const descOk =
          description &&
          typeof description.value === "string" &&
          description.value.trim();
        [title, description].forEach((field) => {
          if (!field) return;
          const row = field.closest(".form-row");
          if (row) row.classList.remove("has-error");
          field.removeAttribute("aria-invalid");
        });
        if (titleOk && descOk && !complete) complete = code;
      });

      if (complete) return true;

      // Highlight active (or first) language tab fields
      const activePanel =
        pane.querySelector(".lang-tabs__panel.is-active") ||
        pane.querySelector("[data-lang-panel]");
      const code = activePanel?.dataset.langPanel || "fa";
      ["title", "description"].forEach((base) => {
        const field = form.elements.namedItem(`${base}_${code}`);
        if (!field || typeof field.value !== "string") return;
        if (!field.value.trim()) {
          field.closest(".form-row")?.classList.add("has-error");
          field.setAttribute("aria-invalid", "true");
        }
      });
      const tip = pane.querySelector("[data-lang-pair-error]");
      if (tip) tip.hidden = false;
      const first = pane.querySelector(".has-error input, .has-error textarea");
      if (first) first.focus();
      return false;
    };

    const validateStep = (n) => {
      const pane = panes.find((p) => Number(p.dataset.wizardStep) === n);
      if (!pane) return true;

      if (pane.dataset.langPairRequired) {
        const tip = pane.querySelector("[data-lang-pair-error]");
        if (tip) tip.hidden = true;
        return validateLangPair(pane);
      }

      let ok = true;
      const required = (pane.dataset.requiredFields || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      required.forEach((name) => {
        const field = form.elements.namedItem(name);
        if (!field || typeof field.value !== "string") return;
        const row = field.closest(".form-row");
        const empty = !field.value.trim();
        if (row) row.classList.toggle("has-error", empty);
        if (empty) {
          ok = false;
          field.setAttribute("aria-invalid", "true");
        } else {
          field.removeAttribute("aria-invalid");
        }
      });

      if (!ok) {
        const first = pane.querySelector(".has-error input, .has-error textarea");
        if (first) first.focus();
      }
      return ok;
    };

    prevBtn?.addEventListener("click", () => showStep(step - 1));

    nextBtn.addEventListener("click", () => {
      if (!validateStep(step)) return;
      showStep(step + 1);
    });

    indicators.forEach((item) => {
      item.addEventListener("click", () => {
        const target = Number(item.dataset.stepIndicator);
        if (target < step) {
          showStep(target);
          return;
        }
        for (let i = step; i < target; i++) {
          if (!validateStep(i)) {
            showStep(i);
            return;
          }
        }
        showStep(target);
      });
      item.style.cursor = "pointer";
    });

    form.addEventListener("submit", (event) => {
      for (let i = 1; i <= total; i++) {
        if (!validateStep(i)) {
          event.preventDefault();
          showStep(i);
          const btn = form.querySelector("button.is-loading");
          if (btn) {
            btn.classList.remove("is-loading");
            btn.removeAttribute("aria-busy");
            btn.querySelector(".spinner-dots")?.remove();
          }
          return;
        }
      }
    });

    initPhotoPreview(root);
    initLangTabs(root);
    showStep(root.dataset.hasErrors ? firstErrorStep() : 1);
    delete root.dataset.hasErrors;
  }

  function initLangTabs(root) {
    const wraps = root.querySelectorAll("[data-lang-tabs]");
    wraps.forEach((wrap) => {
      const buttons = Array.from(wrap.querySelectorAll("[data-lang-tab]"));
      const panels = Array.from(wrap.querySelectorAll("[data-lang-panel]"));
      if (!buttons.length || !panels.length) return;

      const activate = (code) => {
        buttons.forEach((btn) => {
          const on = btn.dataset.langTab === code;
          btn.classList.toggle("is-active", on);
          btn.setAttribute("aria-selected", on ? "true" : "false");
        });
        panels.forEach((panel) => {
          const on = panel.dataset.langPanel === code;
          panel.hidden = !on;
          panel.classList.toggle("is-active", on);
        });
      };

      buttons.forEach((btn) => {
        btn.addEventListener("click", () => activate(btn.dataset.langTab));
      });

      // Open first language tab that has a field error
      const errorPanel = panels.find((p) => p.querySelector(".has-error, .form-error"));
      if (errorPanel) activate(errorPanel.dataset.langPanel);
    });
  }

  function revokeUrls(urls) {
    urls.forEach((url) => URL.revokeObjectURL(url));
    urls.length = 0;
  }

  function initPhotoPreview(root) {
    const wrap = root.querySelector("[data-photo-preview]");
    if (!wrap) return;
    const input = wrap.querySelector('input[type="file"]');
    const placeholder = wrap.querySelector("[data-photo-placeholder]");
    const frame = wrap.querySelector("[data-photo-frame]");
    const strip = wrap.querySelector("[data-photo-strip]");
    if (!input) return;

    const objectUrls = [];
    const isMulti = wrap.hasAttribute("data-multi-photos") || input.multiple;

    const renderMulti = (files) => {
      revokeUrls(objectUrls);
      if (!strip) return;
      strip.innerHTML = "";
      const images = Array.from(files || []).filter((f) => f.type.startsWith("image/"));
      let hero = wrap.querySelector("[data-photo-img]");
      if (!images.length) {
        strip.hidden = true;
        if (hero) {
          hero.hidden = true;
          hero.removeAttribute("src");
        }
        if (placeholder) placeholder.hidden = false;
        frame?.classList.remove("has-image");
        return;
      }
      if (!hero) {
        hero = document.createElement("img");
        hero.setAttribute("data-photo-img", "");
        hero.alt = "";
        frame?.prepend(hero);
      }
      const heroUrl = URL.createObjectURL(images[0]);
      objectUrls.push(heroUrl);
      hero.src = heroUrl;
      hero.hidden = false;
      if (placeholder) placeholder.hidden = true;
      frame?.classList.add("has-image");
      strip.hidden = images.length < 2;
      images.slice(1).forEach((file) => {
        const url = URL.createObjectURL(file);
        objectUrls.push(url);
        const fig = document.createElement("figure");
        fig.className = "wizard-photo__thumb";
        const img = document.createElement("img");
        img.src = url;
        img.alt = "";
        fig.appendChild(img);
        strip.appendChild(fig);
      });
    };

    const showSingle = (file) => {
      if (!file || !file.type.startsWith("image/")) return;
      let img = wrap.querySelector("[data-photo-img]");
      if (!img) {
        img = document.createElement("img");
        img.setAttribute("data-photo-img", "");
        img.alt = "";
        frame?.prepend(img);
      }
      const url = URL.createObjectURL(file);
      const prev = img.dataset.objectUrl;
      if (prev) URL.revokeObjectURL(prev);
      img.dataset.objectUrl = url;
      img.src = url;
      img.hidden = false;
      if (placeholder) placeholder.hidden = true;
      frame?.classList.add("has-image");
    };

    input.addEventListener("change", () => {
      if (isMulti) {
        renderMulti(input.files);
      } else {
        const file = input.files && input.files[0];
        if (file) showSingle(file);
      }
    });

    frame?.addEventListener("click", (event) => {
      if (event.target === input) return;
      input.click();
    });

    const existingImg = wrap.querySelector("[data-photo-img]");
    if (existingImg?.getAttribute("src")) {
      existingImg.hidden = false;
      if (placeholder) placeholder.hidden = true;
      frame?.classList.add("has-image");
    }
  }

  function initBrandModelSelect(root) {
    const mapEl = document.getElementById("brand-model-map");
    const brandSelect = root.querySelector('select[name="brand"]');
    const modelSelect = root.querySelector('select[name="car_model"]');
    if (!mapEl || !brandSelect || !modelSelect) return;

    let map = {};
    try {
      map = JSON.parse(mapEl.textContent || "{}");
    } catch (_err) {
      map = {};
    }

    const emptyLabel =
      modelSelect.querySelector('option[value=""]')?.textContent || "---------";
    const selectedModel = modelSelect.value;

    const refillModels = (brandId, keepSelected) => {
      const models = (brandId && map[String(brandId)]) || [];
      modelSelect.innerHTML = "";
      const empty = document.createElement("option");
      empty.value = "";
      empty.textContent = emptyLabel;
      modelSelect.appendChild(empty);
      models.forEach((item) => {
        const opt = document.createElement("option");
        opt.value = String(item.id);
        opt.textContent = item.name;
        if (keepSelected && String(keepSelected) === String(item.id)) {
          opt.selected = true;
        }
        modelSelect.appendChild(opt);
      });
      modelSelect.disabled = !brandId;
    };

    brandSelect.addEventListener("change", () => {
      refillModels(brandSelect.value, "");
    });

    // Ensure models match current brand on load (keeps server-selected model).
    refillModels(brandSelect.value, selectedModel);
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-listing-wizard]").forEach((root) => {
      initListingWizard(root);
      initBrandModelSelect(root);
    });
  });
})();
