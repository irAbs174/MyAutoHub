"""Language switching helpers."""

from __future__ import annotations

from django.views.i18n import set_language as django_set_language


def set_language(request):
    """Thin wrapper around Django's set_language view."""
    return django_set_language(request)
