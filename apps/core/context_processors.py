from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.core.seo import absolute_url, hreflang_alternates, site_url


def site_nav(request):
    return {
        "nav_items": [
            {"label": _("Emergency"), "url_name": "emergency:list"},
            {"label": _("Pricing"), "url_name": "pricing:list"},
            {"label": _("Marketplace"), "url_name": "marketplace:list"},
            {"label": _("Cars"), "url_name": "cars:list"},
            {"label": _("Places"), "url_name": "places:index"},
            {"label": _("YouTube"), "url_name": "youtube:list"},
            {"label": _("Stories"), "url_name": "stories:list"},
        ],
        "landing_url": getattr(settings, "LANDING_URL", "http://localhost:3000"),
    }


def seo(request):
    """Default SEO context for public templates (canonical, hreflang, OG)."""
    origin = site_url(request)
    path = request.path
    canonical = f"{origin}{path}" if origin else request.build_absolute_uri(path)
    default_image = (
        absolute_url("/static/img/logo.png", request) if origin or request else ""
    )
    descriptions = {
        "fa": (
            "مای‌اتوهاب-اورژانس جاده‌ای، بازار خرید و فروش خودرو، "
            "قیمت‌ها، کاتالوگ و داستان‌های خودرویی."
        ),
        "en": (
            "MyAutoHub-roadside emergency, car marketplace, pricing, "
            "catalog, and automotive stories."
        ),
        "ar": (
            "ماي أوتو هاب-طوارئ على الطريق، سوق سيارات، أسعار، "
            "كتالوج وقصص السيارات."
        ),
    }
    lang = getattr(request, "LANGUAGE_CODE", "fa")[:2]
    return {
        "seo_site_url": origin,
        "seo_canonical": canonical,
        "seo_hreflang": hreflang_alternates(request),
        "seo_default_description": descriptions.get(lang, descriptions["en"]),
        "seo_default_image": default_image,
        "seo_og_locale": {
            "fa": "fa_IR",
            "en": "en_US",
            "ar": "ar_AE",
        }.get(lang, "en_US"),
    }
