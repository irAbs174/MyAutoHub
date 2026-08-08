const THEME_KEY = "myautohub-theme";

function getSystemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function resolveTheme(theme) {
  if (theme === "system") return getSystemTheme();
  if (theme === "dark" || theme === "light") return theme;
  return "dark";
}

function applyTheme(theme) {
  const resolved = resolveTheme(theme);
  document.documentElement.classList.toggle("dark", resolved === "dark");
  document.documentElement.style.colorScheme = resolved;
  return resolved;
}

function getStoredTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "light" || saved === "dark" || saved === "system") {
      return saved;
    }
  } catch (_) {
    /* ignore */
  }
  return "dark";
}

function setStoredTheme(theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch (_) {
    /* ignore */
  }
  return applyTheme(theme);
}

function toggleTheme() {
  const current = resolveTheme(getStoredTheme());
  const next = current === "dark" ? "light" : "dark";
  setStoredTheme(next);
  syncThemeToggle(next);
  return next;
}

function syncThemeToggle(resolved) {
  const btn = document.querySelector("[data-theme-toggle]");
  if (!btn) return;
  const isDark = resolved === "dark";
  btn.classList.toggle("is-dark", isDark);
  btn.setAttribute("aria-pressed", isDark ? "true" : "false");
  btn.setAttribute(
    "aria-label",
    isDark
      ? btn.dataset.labelLight || "Light theme"
      : btn.dataset.labelDark || "Dark theme",
  );
}

function initReveals() {
  const nodes = document.querySelectorAll(".reveal");
  if (!nodes.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  if (!("IntersectionObserver" in window)) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
  );

  nodes.forEach((el) => io.observe(el));
}

function makeDotSpinner(extraClass) {
  const wrap = document.createElement("span");
  wrap.className =
    "spinner-dots spinner-dots--sm" + (extraClass ? " " + extraClass : "");
  wrap.setAttribute("aria-hidden", "true");
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    dot.className = "spinner-dots__dot";
    wrap.appendChild(dot);
  }
  return wrap;
}

const MEDIA_LOADER_HOSTS =
  ".media-thumb, .gallery-hero, .gallery-strip figure, .story-cover, .car-gallery-hero, .car-gallery-thumb";

function finishMediaLoader(host, img) {
  host.classList.remove("is-loading");
  host.classList.add("is-loaded");
  host.removeAttribute("aria-busy");
  if (img) img.removeAttribute("aria-busy");
  const loader = host.querySelector("[data-media-loader]");
  if (loader) loader.remove();
}

function showMediaLoader(host, img) {
  if (host.classList.contains("is-loaded") || host.classList.contains("is-loading")) {
    return;
  }
  if (img.complete) {
    finishMediaLoader(host, img);
    return;
  }

  host.classList.add("is-loading");
  host.setAttribute("aria-busy", "true");
  img.setAttribute("aria-busy", "true");

  if (!host.querySelector("[data-media-loader]")) {
    const loader = document.createElement("span");
    loader.className = "media-loader";
    loader.setAttribute("data-media-loader", "");
    loader.setAttribute("aria-hidden", "true");
    loader.appendChild(makeDotSpinner());
    host.appendChild(loader);
  }

  const done = () => finishMediaLoader(host, img);
  img.addEventListener("load", done, { once: true });
  img.addEventListener("error", done, { once: true });
}

function initMediaLoaders() {
  const hosts = document.querySelectorAll(MEDIA_LOADER_HOSTS);
  if (!hosts.length) return;

  const attach = (host) => {
    const img = host.querySelector("img");
    if (!img) return;
    showMediaLoader(host, img);
  };

  if (!("IntersectionObserver" in window)) {
    hosts.forEach(attach);
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        attach(entry.target);
        io.unobserve(entry.target);
      });
    },
    { rootMargin: "80px 0px", threshold: 0.01 },
  );

  hosts.forEach((host) => {
    const img = host.querySelector("img");
    if (!img) return;
    if (img.complete) {
      finishMediaLoader(host, img);
      return;
    }
    io.observe(host);
  });
}

function initNavSearch() {
  const form = document.querySelector("[data-nav-search]");
  if (!form) return;

  const input = form.querySelector("[data-nav-search-input]");
  const btn = form.querySelector("[data-nav-search-btn]");
  const panel = form.querySelector("[data-nav-search-results]");
  if (!input || !btn || !panel) return;

  const suggestUrl = form.dataset.suggestUrl || "/api/public/search/";
  const noResultsLabel = form.dataset.noResults || "No matches found";
  // Compact icon search expands on both desktop and mobile.
  const useIconSearch = () => true;

  let results = [];
  let activeIndex = -1;
  let debounceTimer = 0;
  let abortController = null;
  let blurTimer = 0;

  const open = () => {
    form.classList.add("is-open");
    input.focus();
  };

  const closeShell = () => {
    if (input.value.trim()) return;
    form.classList.remove("is-open");
  };

  const setExpanded = (openPanel) => {
    input.setAttribute("aria-expanded", openPanel ? "true" : "false");
    panel.hidden = !openPanel;
  };

  const hidePanel = () => {
    setExpanded(false);
    activeIndex = -1;
  };

  const selectResult = (result) => {
    if (!result || !result.url) return;
    window.location.href = result.url;
  };

  const renderResults = () => {
    panel.replaceChildren();

    if (!results.length) {
      const empty = document.createElement("p");
      empty.className = "nav-search-empty";
      empty.textContent = noResultsLabel;
      panel.appendChild(empty);
      setExpanded(true);
      return;
    }

    results.forEach((result, i) => {
      const option = document.createElement("button");
      option.type = "button";
      option.className = "nav-search-option";
      option.setAttribute("role", "option");
      option.setAttribute("aria-selected", i === activeIndex ? "true" : "false");
      if (i === activeIndex) option.classList.add("is-active");

      const category = document.createElement("span");
      category.className = "nav-search-option-category";
      category.textContent = result.category_label || result.category || "";

      const title = document.createElement("span");
      title.className = "nav-search-option-title";
      title.textContent = result.title || "";

      option.appendChild(category);
      option.appendChild(title);

      if (result.subtitle) {
        const subtitle = document.createElement("span");
        subtitle.className = "nav-search-option-subtitle";
        subtitle.textContent = result.subtitle;
        option.appendChild(subtitle);
      }

      option.addEventListener("mouseenter", () => {
        activeIndex = i;
        syncActive();
      });
      option.addEventListener("mousedown", (event) => {
        event.preventDefault();
        selectResult(result);
      });

      panel.appendChild(option);
    });

    setExpanded(true);
  };

  const syncActive = () => {
    panel.querySelectorAll(".nav-search-option").forEach((el, i) => {
      const on = i === activeIndex;
      el.classList.toggle("is-active", on);
      el.setAttribute("aria-selected", on ? "true" : "false");
    });
  };

  const fetchSuggest = (q) => {
    if (abortController) abortController.abort();
    if (!q) {
      results = [];
      hidePanel();
      return;
    }

    abortController = new AbortController();
    const url = `${suggestUrl}?q=${encodeURIComponent(q)}`;

    fetch(url, {
      signal: abortController.signal,
      headers: { Accept: "application/json" },
    })
      .then((res) => {
        if (!res.ok) throw new Error("suggest failed");
        return res.json();
      })
      .then((data) => {
        results = Array.isArray(data.results) ? data.results : [];
        activeIndex = results.length ? 0 : -1;
        renderResults();
      })
      .catch((err) => {
        if (err && err.name === "AbortError") return;
        results = [];
        hidePanel();
      });
  };

  const scheduleSuggest = () => {
    window.clearTimeout(debounceTimer);
    const q = input.value.trim();
    if (!q) {
      results = [];
      hidePanel();
      return;
    }
    debounceTimer = window.setTimeout(() => fetchSuggest(q), 180);
  };

  if (useIconSearch() && input.value.trim()) {
    form.classList.add("is-open");
  }

  btn.addEventListener("click", (event) => {
    if (!useIconSearch()) return;
    const expanded =
      form.classList.contains("is-open") || form.matches(":focus-within");
    if (expanded && input.value.trim()) return;
    event.preventDefault();
    open();
  });

  input.addEventListener("focus", () => {
    if (useIconSearch()) form.classList.add("is-open");
    if (input.value.trim() && results.length) setExpanded(true);
    else if (input.value.trim()) scheduleSuggest();
  });

  input.addEventListener("input", scheduleSuggest);

  input.addEventListener("blur", () => {
    window.clearTimeout(blurTimer);
    blurTimer = window.setTimeout(() => {
      hidePanel();
      closeShell();
    }, 140);
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      if (!results.length) return;
      event.preventDefault();
      activeIndex = (activeIndex + 1) % results.length;
      syncActive();
      setExpanded(true);
      return;
    }
    if (event.key === "ArrowUp") {
      if (!results.length) return;
      event.preventDefault();
      activeIndex = (activeIndex - 1 + results.length) % results.length;
      syncActive();
      setExpanded(true);
      return;
    }
    if (event.key === "Enter") {
      if (panel.hidden || !results.length || activeIndex < 0) return;
      event.preventDefault();
      selectResult(results[activeIndex] || results[0]);
      return;
    }
    if (event.key === "Escape") {
      if (!panel.hidden) {
        event.preventDefault();
        hidePanel();
        return;
      }
      input.blur();
      form.classList.remove("is-open");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && form.contains(document.activeElement)) {
      if (!panel.hidden) {
        hidePanel();
        return;
      }
      input.blur();
      form.classList.remove("is-open");
    }
  });
}

function initExpertSlider() {
  document.querySelectorAll("[data-expert-slider]").forEach((root) => {
    const track = root.querySelector("[data-expert-track]");
    const prev = root.querySelector("[data-expert-prev]");
    const next = root.querySelector("[data-expert-next]");
    if (!track || !prev || !next) return;

    const isRtl = () => document.documentElement.getAttribute("dir") === "rtl";

    const slideStep = () => {
      const first = track.querySelector(".home-expert-slide");
      if (!first) return track.clientWidth;
      const styles = getComputedStyle(track);
      const gap = parseFloat(styles.columnGap || styles.gap) || 0;
      return first.getBoundingClientRect().width + gap;
    };

    const maxScroll = () =>
      Math.max(0, track.scrollWidth - track.clientWidth);

    const canScrollToward = (dir) => {
      const max = maxScroll();
      const epsilon = 4;
      if (max <= epsilon) return false;

      const x = track.scrollLeft;
      // Chromium RTL often keeps scrollLeft in 0..max; Firefox uses negatives.
      if (isRtl() && x < 0) {
        return dir < 0
          ? Math.abs(x) < max - epsilon
          : Math.abs(x) > epsilon;
      }
      return dir < 0 ? x > epsilon : x < max - epsilon;
    };

    const syncButtons = () => {
      prev.disabled = !canScrollToward(-1);
      next.disabled = !canScrollToward(1);
    };

    const scrollByDir = (dir) => {
      const delta = slideStep() * dir * (isRtl() ? -1 : 1);
      track.scrollBy({ left: delta, behavior: "smooth" });
    };

    prev.addEventListener("click", () => scrollByDir(-1));
    next.addEventListener("click", () => scrollByDir(1));
    track.addEventListener("scroll", syncButtons, { passive: true });
    window.addEventListener("resize", syncButtons);
    syncButtons();
  });
}

function initMobileNav() {
  const header = document.querySelector("[data-site-header]");
  const burger = document.querySelector("[data-nav-burger]");
  const drawer = document.querySelector("[data-nav-drawer]");
  if (!header || !burger || !drawer) return;

  const mq = window.matchMedia("(max-width: 760px)");
  const labelOpen = burger.dataset.labelOpen || "Open menu";
  const labelClose = burger.dataset.labelClose || "Close menu";

  const setOpen = (open) => {
    header.classList.toggle("is-nav-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? labelClose : labelOpen);
  };

  burger.addEventListener("click", () => {
    setOpen(!header.classList.contains("is-nav-open"));
  });

  drawer.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setOpen(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });

  const onMq = () => {
    if (!mq.matches) setOpen(false);
  };
  if (mq.addEventListener) mq.addEventListener("change", onMq);
  else mq.addListener(onMq);
}

document.addEventListener("DOMContentLoaded", () => {
  const resolved = applyTheme(getStoredTheme());
  syncThemeToggle(resolved);
  initReveals();
  initMediaLoaders();
  initNavSearch();
  initMobileNav();
  initExpertSlider();
  const themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => toggleTheme());
  }

  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      if (getStoredTheme() === "system") {
        syncThemeToggle(applyTheme("system"));
      }
    });

  const modeRadios = document.querySelectorAll('input[name="location_mode"]');
  const mapFields = document.querySelector("[data-map-fields]");
  const savedFields = document.querySelector("[data-saved-fields]");

  // Emergency submit page owns its own map + mode sync in emergency-map.js
  if (
    modeRadios.length &&
    mapFields &&
    savedFields &&
    !document.querySelector("[data-emergency-map]")
  ) {
    const sync = (mode) => {
      const useSaved = mode === "saved";
      mapFields.hidden = useSaved;
      savedFields.hidden = !useSaved;
      mapFields.querySelectorAll("input").forEach((el) => {
        el.disabled = useSaved;
      });
      savedFields.querySelectorAll("select").forEach((el) => {
        el.disabled = !useSaved;
      });
    };

    modeRadios.forEach((el) => {
      el.addEventListener("change", () => sync(el.value));
      if (el.checked) sync(el.value);
    });
  }

  document.querySelectorAll("[data-buzz-form]").forEach((form) => {
    form.addEventListener("submit", () => {
      const target = document.querySelector("[data-buzz-target]");
      if (target) target.classList.add("buzz-pulse");
    });
  });

  document.querySelectorAll("[data-lang-tabs]").forEach((wrap) => {
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

    const errorPanel = panels.find((p) => p.querySelector(".has-error, .form-error"));
    if (errorPanel) activate(errorPanel.dataset.langPanel);
  });

  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      if (form.matches("[data-nav-search]")) return;
      const btn = form.querySelector(
        'button[type="submit"]:not([disabled]), input[type="submit"]:not([disabled])',
      );
      if (!btn || btn.classList.contains("is-loading")) return;
      btn.classList.add("is-loading");
      btn.setAttribute("aria-busy", "true");
      if (btn.tagName === "BUTTON" && !btn.querySelector(".spinner-dots")) {
        const onAccent = !btn.classList.contains("btn-ghost");
        btn.appendChild(
          makeDotSpinner(onAccent ? "spinner-dots--on-accent" : ""),
        );
      }
    });
  });

  // Dismissible learn tips (per tip_id in localStorage)
  const TIP_PREFIX = "myautohub-tip-dismissed:";
  document.querySelectorAll("[data-learn-tip]").forEach((tip) => {
    const id = tip.getAttribute("data-tip-id");
    if (!id) return;
    let dismissed = false;
    try {
      dismissed = localStorage.getItem(TIP_PREFIX + id) === "1";
    } catch (e) {
      dismissed = false;
    }
    if (dismissed) {
      tip.hidden = true;
      return;
    }
    tip.hidden = false;
    const btn = tip.querySelector("[data-learn-tip-dismiss]");
    if (!btn) return;
    btn.addEventListener("click", () => {
      tip.hidden = true;
      try {
        localStorage.setItem(TIP_PREFIX + id, "1");
      } catch (e) {
        /* ignore quota / private mode */
      }
    });
  });

  initBackToTop();
});

function initBackToTop() {
  const btn = document.querySelector("[data-back-to-top]");
  if (!btn) return;

  const threshold = 420;
  const sync = () => {
    const show = window.scrollY > threshold;
    btn.hidden = !show;
    btn.classList.toggle("is-visible", show);
  };

  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(() => {
        sync();
        ticking = false;
      });
    },
    { passive: true },
  );

  btn.addEventListener("click", () => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });

  sync();
}