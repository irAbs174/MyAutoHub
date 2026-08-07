from django import template

from apps.core.i18n_content import localized

register = template.Library()


@register.filter(name="localized")
def localized_filter(obj, base: str) -> str:
    """Resolve a trilingual field: ``{{ item|localized:"title" }}``."""
    if obj is None:
        return ""
    return localized(obj, base)
