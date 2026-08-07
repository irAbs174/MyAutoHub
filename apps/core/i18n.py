"""Language switching helpers."""

from __future__ import annotations

import json
import time
from pathlib import Path

from django.views.i18n import set_language as django_set_language

# #region agent log
_DEBUG_LOG = Path("/home/unique/Documents/projects/Production/myautohub/.cursor/debug-06ccaa.log")


def _agent_log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    try:
        payload = {
            "sessionId": "06ccaa",
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with _DEBUG_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass


# #endregion


def set_language(request):
    """Thin wrapper around Django's set_language view."""
    # #region agent log
    _agent_log(
        "C",
        "apps/core/i18n.py:set_language:entry",
        "set_language POST",
        {
            "method": request.method,
            "language": request.POST.get("language"),
            "next": request.POST.get("next"),
            "path": request.path,
            "cookie_before": request.COOKIES.get("django_language"),
        },
    )
    # #endregion
    response = django_set_language(request)
    # #region agent log
    set_cookie = None
    if hasattr(response, "cookies") and "django_language" in response.cookies:
        set_cookie = response.cookies["django_language"].value
    _agent_log(
        "C",
        "apps/core/i18n.py:set_language:exit",
        "set_language response",
        {
            "status": getattr(response, "status_code", None),
            "location": response.get("Location") if hasattr(response, "get") else None,
            "cookie_set": set_cookie,
        },
    )
    # #endregion
    return response
