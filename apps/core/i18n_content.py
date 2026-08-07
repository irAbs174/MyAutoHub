from django.utils.translation import get_language

CONTENT_LANGS = ("fa", "en", "ar")


def localized(obj, base: str, lang=None) -> str:
    """Return the best available translation for ``base`` on ``obj``.

    Looks up ``{base}_{lang}`` for the active language, then fa, en, ar.
    """
    lang = (lang or get_language() or "fa")[:2]
    for code in (lang, "fa", "en", "ar"):
        val = getattr(obj, f"{base}_{code}", None)
        if val:
            return val
    return ""


def tri(base: str, text: str) -> dict:
    """Expand one string into ``{base}_fa/_en/_ar`` kwargs for model create/update."""
    value = text or ""
    return {f"{base}_fa": value, f"{base}_en": value, f"{base}_ar": value}


def tri_fields(**fields: str) -> dict:
    """Expand multiple base→text pairs into trilingual kwargs."""
    out = {}
    for base, text in fields.items():
        out.update(tri(base, text))
    return out


def localized_attr(base: str):
    """Descriptor that resolves ``obj.{base}`` via :func:`localized`."""

    def getter(self):
        return localized(self, base)

    return property(getter)
