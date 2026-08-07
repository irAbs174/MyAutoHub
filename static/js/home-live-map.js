/**
 * Home Live Map preview — MapUp tiles + styled sample pins.
 * Clicking the map (empty area) or Enter on focused canvas opens the CTA URL.
 */
(function () {
  var TILE_URL = "https://tiles.mapup.ir/styles/basic-preview/{z}/{x}/{y}.png";
  var TILE_ATTR =
    '&copy; <a href="https://mapup.ir" target="_blank" rel="noopener">MapUp</a>';

  // Sample activity around Tehran (preview only — not live user data).
  var SAMPLE_PINS = [
    { lat: 35.7219, lng: 51.3347, kind: "emergency" },
    { lat: 35.6997, lng: 51.338, kind: "emergency" },
    { lat: 35.6892, lng: 51.389, kind: "market" },
    { lat: 35.7575, lng: 51.41, kind: "market" },
    { lat: 35.715, lng: 51.405, kind: "alt" },
  ];

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function clearLoading(mapEl) {
    if (!mapEl) return;
    mapEl.classList.remove("is-loading");
    mapEl.removeAttribute("aria-busy");
    var stage = mapEl.closest(".home-live-map-stage");
    var loader = stage ? qs("[data-home-map-loader]", stage) : null;
    if (loader) loader.hidden = true;
  }

  function pinIcon(kind) {
    return L.divIcon({
      className: "home-map-marker home-map-marker--" + kind,
      html: '<span class="home-map-marker-dot"></span>',
      iconSize: [22, 22],
      iconAnchor: [11, 22],
    });
  }

  function init() {
    var mapEl = qs("[data-home-live-map]");
    if (!mapEl || typeof L === "undefined") return;

    var iconBase = mapEl.getAttribute("data-leaflet-icon-base");
    if (iconBase) {
      L.Icon.Default.prototype.options.iconUrl = iconBase + "marker-icon.png";
      L.Icon.Default.prototype.options.iconRetinaUrl =
        iconBase + "marker-icon-2x.png";
      L.Icon.Default.prototype.options.shadowUrl = iconBase + "marker-shadow.png";
    }

    var lat = Number(mapEl.getAttribute("data-default-lat")) || 35.6892;
    var lng = Number(mapEl.getAttribute("data-default-lng")) || 51.389;
    var zoom = Number(mapEl.getAttribute("data-zoom")) || 12;
    var ctaUrl = mapEl.getAttribute("data-cta-url") || "";

    var map = L.map(mapEl, {
      center: [lat, lng],
      zoom: zoom,
      scrollWheelZoom: false,
      attributionControl: true,
      zoomControl: true,
    });

    L.tileLayer(TILE_URL, {
      maxZoom: 18,
      minZoom: 5,
      attribution: TILE_ATTR,
    }).addTo(map);

    SAMPLE_PINS.forEach(function (pin) {
      L.marker([pin.lat, pin.lng], {
        icon: pinIcon(pin.kind),
        keyboard: false,
        interactive: false,
      }).addTo(map);
    });

    map.whenReady(function () {
      clearLoading(mapEl);
      setTimeout(function () {
        map.invalidateSize();
      }, 60);
    });

    map.on("click", function () {
      if (ctaUrl) window.location.href = ctaUrl;
    });

    mapEl.addEventListener("keydown", function (ev) {
      if ((ev.key === "Enter" || ev.key === " ") && ctaUrl) {
        ev.preventDefault();
        window.location.href = ctaUrl;
      }
    });

    // Keep tiles sized after theme toggle / font load.
    window.addEventListener("resize", function () {
      map.invalidateSize();
    });

    var themeBtn = qs("[data-theme-toggle]");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        setTimeout(function () {
          map.invalidateSize();
        }, 80);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
