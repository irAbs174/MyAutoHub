from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page

from apps.core.i18n import set_language
from apps.core.sitemaps import SITEMAPS
from apps.core.views import robots_txt

urlpatterns = [
    path("unique/", admin.site.urls),
    path("panel/", include("apps.panel.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("api/emergency/", include("apps.emergency.api_urls")),
    path("api/public/", include("apps.core.api_urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        cache_page(60 * 60)(sitemap),
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

urlpatterns += i18n_patterns(
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("emergency/", include("apps.emergency.urls")),
    path("pricing/", include("apps.pricing.urls")),
    path("marketplace/", include("apps.marketplace.urls")),
    path("cars/", include("apps.cars.urls")),
    path("places/", include("apps.cars.place_urls")),
    path("youtube/", include("apps.youtube.urls")),
    path("stories/", include("apps.stories.urls")),
    prefix_default_language=True,
)

handler400 = "apps.core.views.bad_request"
handler403 = "apps.core.views.permission_denied"
handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
