"""SEO helpers: absolute URLs, truncated descriptions, hreflang alternates."""

from __future__ import annotations

from urllib.parse import urljoin

from django.conf import settings
from django.urls import translate_url
from django.utils.html import strip_tags
from django.utils.text import Truncator


def site_url(request=None) -> str:
    configured = getattr(settings, "SITE_URL", "") or ""
    configured = configured.rstrip("/")
    if configured:
        return configured
    if request is not None:
        return f"{request.scheme}://{request.get_host()}"
    return ""


def absolute_url(path_or_url: str, request=None) -> str:
    if not path_or_url:
        return ""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    base = site_url(request)
    if not base:
        return path_or_url
    return urljoin(base + "/", path_or_url.lstrip("/"))


def absolute_media_url(file_field, request=None) -> str:
    if not file_field:
        return ""
    try:
        url = file_field.url
    except (ValueError, AttributeError):
        return ""
    return absolute_url(url, request)


def meta_description(text: str, length: int = 160) -> str:
    cleaned = " ".join(strip_tags(text or "").split())
    if not cleaned:
        return ""
    return Truncator(cleaned).chars(length, truncate="…")


def hreflang_alternates(request) -> list[dict[str, str]]:
    """Build alternate language URLs for the current path via translate_url."""
    languages = [code for code, _ in settings.LANGUAGES]
    current = request.build_absolute_uri(request.path)
    base = site_url(request)
    alternates: list[dict[str, str]] = []
    for lang in languages:
        translated = translate_url(current, lang)
        if base and translated.startswith(("http://", "https://")):
            # Keep host from SITE_URL when configured
            from urllib.parse import urlparse

            parsed = urlparse(translated)
            url = f"{base}{parsed.path}"
            if parsed.query:
                url = f"{url}?{parsed.query}"
        else:
            url = translated
        alternates.append({"lang": lang, "url": url})
    # x-default → default language (fa)
    default_lang = settings.LANGUAGE_CODE
    default = next((a for a in alternates if a["lang"] == default_lang), None)
    if default:
        alternates.append({"lang": "x-default", "url": default["url"]})
    return alternates
