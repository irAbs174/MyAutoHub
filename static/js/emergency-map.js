/**
 * Leaflet click-to-pin + geolocation for emergency submit and saved locations.
 * Uses locally vendored Leaflet + MapUp tiles (fast Iran CDN).
 * Requires Leaflet global `L` and a `[data-emergency-map]` or `[data-location-map]` container.
 */
(function () {
  // MapUp-ArvanCloud Iran tiles (no API key). Faster/reliable vs OSM.org tiles.
  var TILE_URL = "https://tiles.mapup.ir/styles/basic-preview/{z}/{x}/{y}.png";
  var TILE_ATTR = '&copy; <a href="https://mapup.ir" target="_blank" rel="noopener">MapUp</a>';
  var TILE_OPTS = { maxZoom: 20, minZoom: 5, attribution: TILE_ATTR };

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.from((root || document).querySelectorAll(sel));
  }

  function toNum(v) {
    // Number("") === 0-treat blank inputs as missing, not Null Island.
    if (v == null) return null;
    const s = String(v).trim();
    if (s === "") return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  }

  function showMapError(mapEl, message) {
    if (!mapEl) return;
    clearMapLoading(mapEl);
    mapEl.setAttribute("data-map-error", "1");
    mapEl.textContent = message;
  }

  function clearMapLoading(mapEl) {
    if (!mapEl) return;
    mapEl.classList.remove("is-loading");
    mapEl.removeAttribute("aria-busy");
    const stage = mapEl.closest(".map-stage") || mapEl.parentElement;
    const loader = stage
      ? qs("[data-map-loader], .emergency-map-loader", stage)
      : qs(".emergency-map-loader", mapEl);
    if (loader) loader.remove();
  }

  function makeDotSpinner(extraClass) {
    const wrap = document.createElement("span");
    wrap.className = "spinner-dots spinner-dots--sm" + (extraClass ? " " + extraClass : "");
    wrap.setAttribute("aria-hidden", "true");
    for (let i = 0; i < 3; i++) {
      const dot = document.createElement("span");
      dot.className = "spinner-dots__dot";
      wrap.appendChild(dot);
    }
    return wrap;
  }

  function setButtonLoading(btn, loading) {
    if (!btn) return;
    if (loading) {
      if (btn.dataset.loading === "1") return;
      btn.dataset.loading = "1";
      btn.disabled = true;
      btn.classList.add("is-loading");
      if (!qs(".spinner-dots", btn)) {
        btn.appendChild(makeDotSpinner());
      }
    } else {
      btn.dataset.loading = "0";
      btn.disabled = false;
      btn.classList.remove("is-loading");
      const spinner = qs(".spinner-dots", btn);
      if (spinner) spinner.remove();
    }
  }

  function initEmergencyMap() {
    const mapEl = qs("[data-emergency-map], [data-location-map]");
    if (!mapEl) return;

    if (typeof L === "undefined") {
      showMapError(
        mapEl,
        "Map failed to load. Refresh the page and try again.",
      );
      return;
    }

    const latInput = qs(mapEl.dataset.latInput || "#id_latitude");
    const lngInput = qs(mapEl.dataset.lngInput || "#id_longitude");
    const hint = qs("[data-map-hint]");
    const locateBtn = qs("[data-map-locate]");
    const mapFields = qs("[data-map-fields]");
    const savedFields = qs("[data-saved-fields]");

    const defaultLat = toNum(mapEl.dataset.defaultLat) ?? 35.6892;
    const defaultLng = toNum(mapEl.dataset.defaultLng) ?? 51.389;
    const inputLat = toNum(latInput && latInput.value);
    const inputLng = toNum(lngInput && lngInput.value);
    // Real saved coords only-blank NumberInput values must not become 0/0.
    let hadInitial = Boolean(inputLat != null && inputLng != null);
    if (hadInitial && Math.abs(inputLat) < 1e-9 && Math.abs(inputLng) < 1e-9) {
      hadInitial = false;
    }
    let lat = hadInitial ? inputLat : defaultLat;
    let lng = hadInitial ? inputLng : defaultLng;

    // Leaflet Default always prepends imagePath to relative icon filenames —
    // set the base only; absolute iconUrl values get doubled and break the pin.
    const iconBase = mapEl.dataset.leafletIconBase;
    if (iconBase) {
      L.Icon.Default.imagePath = iconBase.endsWith("/")
        ? iconBase
        : iconBase + "/";
    }

    let map;
    try {
      map = L.map(mapEl, {
        scrollWheelZoom: true,
        zoomControl: true,
      }).setView([lat, lng], hadInitial ? 15 : 12);
    } catch (err) {
      showMapError(
        mapEl,
        "Map failed to initialize. Refresh the page and try again.",
      );
      return;
    }

    clearMapLoading(mapEl);

    L.tileLayer(TILE_URL, TILE_OPTS).addTo(map);

    let marker = null;

    function setHint(text) {
      if (hint) hint.textContent = text;
    }

    function writeInputs(nextLat, nextLng) {
      if (latInput) latInput.value = nextLat.toFixed(6);
      if (lngInput) lngInput.value = nextLng.toFixed(6);
    }

    function placePin(nextLat, nextLng, opts) {
      lat = nextLat;
      lng = nextLng;
      writeInputs(nextLat, nextLng);
      if (marker) {
        marker.setLatLng([nextLat, nextLng]);
      } else {
        marker = L.marker([nextLat, nextLng], { draggable: true }).addTo(map);
        marker.on("dragend", () => {
          const p = marker.getLatLng();
          placePin(p.lat, p.lng, { silent: true });
          setHint("Pin moved-coordinates updated.");
        });
      }
      if (!opts || !opts.silent) {
        map.panTo([nextLat, nextLng]);
      }
    }

    if (hadInitial) {
      placePin(lat, lng, { silent: true });
      setHint("Pin set. Drag it or tap elsewhere to move.");
    }

    map.on("click", (e) => {
      placePin(e.latlng.lat, e.latlng.lng);
      setHint("Pin dropped. Drag to fine-tune.");
    });

    if (locateBtn) {
      locateBtn.addEventListener("click", () => {
        if (!navigator.geolocation) {
          setHint("Geolocation is not available in this browser.");
          return;
        }
        setButtonLoading(locateBtn, true);
        setHint("Finding your location…");
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            setButtonLoading(locateBtn, false);
            const { latitude, longitude } = pos.coords;
            placePin(latitude, longitude);
            map.setZoom(16);
            setHint("Using your current location.");
          },
          () => {
            setButtonLoading(locateBtn, false);
            setHint("Could not get location-tap the map instead.");
          },
          { enableHighAccuracy: true, timeout: 12000 },
        );
      });
    }

    // Keep Leaflet sized when the map panel is shown/hidden.
    function invalidateSoon() {
      window.setTimeout(() => map.invalidateSize(), 60);
    }

    function syncLocationMode(mode) {
      const useSaved = mode === "saved";
      if (mapFields) mapFields.hidden = useSaved;
      if (savedFields) savedFields.hidden = !useSaved;
      if (mapFields) {
        mapFields.querySelectorAll("input").forEach((el) => {
          el.disabled = useSaved;
        });
      }
      if (savedFields) {
        savedFields.querySelectorAll("select").forEach((el) => {
          el.disabled = !useSaved;
        });
      }
      // #region agent log
      (function () {
        const sel = savedFields && savedFields.querySelector("select");
        const savedCs =
          savedFields && window.getComputedStyle
            ? window.getComputedStyle(savedFields)
            : null;
        fetch(
          "http://127.0.0.1:7280/ingest/36ac9add-62dd-4ea2-86a0-df3c6a9bcd69",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Debug-Session-Id": "5a4dd4",
            },
            body: JSON.stringify({
              sessionId: "5a4dd4",
              hypothesisId: "B,C,D,E",
              location: "emergency-map.js:syncLocationMode",
              message: "location mode sync",
              data: {
                mode: mode,
                useSaved: useSaved,
                hasSavedFields: Boolean(savedFields),
                savedHiddenAttr: savedFields
                  ? savedFields.hasAttribute("hidden")
                  : null,
                savedDisplay: savedCs ? savedCs.display : null,
                selectDisabled: sel ? sel.disabled : null,
                optionCount: sel ? sel.options.length : null,
                optionTexts: sel
                  ? Array.from(sel.options).map(function (o) {
                      return o.text;
                    })
                  : [],
                selectedValue: sel ? sel.value : null,
              },
              timestamp: Date.now(),
              runId: "pre-fix",
            }),
          },
        ).catch(function () {});
      })();
      // #endregion
      if (!useSaved) invalidateSoon();
    }

    const modeRadios = qsa('input[name="location_mode"]');
    // #region agent log
    fetch("http://127.0.0.1:7280/ingest/36ac9add-62dd-4ea2-86a0-df3c6a9bcd69", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Debug-Session-Id": "5a4dd4",
      },
      body: JSON.stringify({
        sessionId: "5a4dd4",
        hypothesisId: "C",
        location: "emergency-map.js:init",
        message: "mode radios found",
        data: {
          radioCount: modeRadios.length,
          radioValues: modeRadios.map(function (el) {
            return { value: el.value, checked: el.checked };
          }),
          hasSavedFields: Boolean(savedFields),
          hasMapFields: Boolean(mapFields),
        },
        timestamp: Date.now(),
        runId: "pre-fix",
      }),
    }).catch(function () {});
    // #endregion
    modeRadios.forEach((el) => {
      el.addEventListener("change", () => syncLocationMode(el.value));
      if (el.checked) syncLocationMode(el.value);
    });

    if (!modeRadios.length) {
      syncLocationMode("map");
    }

    // Manual coord edits move the pin.
    function syncFromInputs() {
      const nextLat = toNum(latInput && latInput.value);
      const nextLng = toNum(lngInput && lngInput.value);
      if (nextLat == null || nextLng == null) return;
      if (Math.abs(nextLat - lat) < 1e-7 && Math.abs(nextLng - lng) < 1e-7) return;
      placePin(nextLat, nextLng);
    }
    if (latInput) latInput.addEventListener("change", syncFromInputs);
    if (lngInput) lngInput.addEventListener("change", syncFromInputs);

    invalidateSoon();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEmergencyMap);
  } else {
    initEmergencyMap();
  }
})();
