import os

# Load production when DJANGO_ENV=production (custom error pages require DEBUG=False).
# Otherwise use local settings (DEBUG on for development).
if os.environ.get("DJANGO_ENV", "local").lower() == "production":
    from .production import *  # noqa: F401,F403
else:
    from .local import *  # noqa: F401,F403
