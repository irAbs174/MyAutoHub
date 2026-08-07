from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _

from apps.cars.models import Car, CarPhoto
from apps.emergency.models import EmergencyService
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

from .search import run_search


def _error_home_url():
    """Safe home link for error pages (never raise during error handling)."""
    try:
        return reverse("core:home")
    except NoReverseMatch:
        return "/"


def _render_error(request, template, *, code, title, message, status):
    return render(
        request,
        template,
        {
            "error_code": code,
            "error_title": title,
            "error_message": message,
            "home_url": _error_home_url(),
        },
        status=status,
    )


def home(request):
    latest_cars = (
        Car.objects.filter(is_published=True)
        .select_related("model__brand")
        .prefetch_related("photos")[:6]
    )
    has_photo = Exists(CarPhoto.objects.filter(car_id=OuterRef("pk")))
    expert_cars = (
        Car.objects.filter(is_published=True)
        .filter(Q(cover_image__gt="") | has_photo)
        .select_related("model__brand")
        .prefetch_related("photos")[:8]
    )
    latest_listings = (
        Listing.objects.filter(status=ListingStatus.ACTIVE)
        .select_related("seller")
        .prefetch_related("photos")[:4]
    )
    latest_videos = YoutubeVideo.objects.filter(is_published=True)[:4]
    latest_stories = Story.objects.filter(is_published=True).select_related("author")[:3]
    price_teasers = (
        PriceReference.objects.filter(is_published=True).prefetch_related("photos")[:4]
    )
    emergency_services = EmergencyService.objects.filter(is_active=True)[:4]

    social_links = getattr(
        settings,
        "SOCIAL_LINKS",
        [
            {"name": "Instagram", "url": "https://instagram.com/", "key": "instagram"},
            {"name": "YouTube", "url": "https://youtube.com/", "key": "youtube"},
            {"name": "Telegram", "url": "https://t.me/", "key": "telegram"},
            {"name": "X", "url": "https://x.com/", "key": "x"},
        ],
    )

    return render(
        request,
        "core/home.html",
        {
            "latest_cars": latest_cars,
            "expert_cars": expert_cars,
            "latest_listings": latest_listings,
            "latest_videos": latest_videos,
            "latest_stories": latest_stories,
            "price_teasers": price_teasers,
            "emergency_services": emergency_services,
            "social_links": social_links,
        },
    )


def search(request):
    q = (request.GET.get("q") or "").strip()
    buckets = run_search(q)
    total = sum(len(v) for v in buckets.values())

    return render(
        request,
        "core/search.html",
        {
            "q": q,
            "total": total,
            "cars": buckets["cars"],
            "listings": buckets["listings"],
            "stories": buckets["stories"],
            "videos": buckets["videos"],
            "prices": buckets["prices"],
            "services": buckets["services"],
        },
    )


def bad_request(request, exception=None):
    return _render_error(
        request,
        "400.html",
        code="400",
        title=_("Bad request"),
        message=_("The request could not be understood. Please try again."),
        status=400,
    )


def permission_denied(request, exception=None):
    return _render_error(
        request,
        "403.html",
        code="403",
        title=_("Access denied"),
        message=_("You do not have permission to view this page."),
        status=403,
    )


def page_not_found(request, exception=None):
    return _render_error(
        request,
        "404.html",
        code="404",
        title=_("Page not found"),
        message=_("This road does not lead anywhere. Head back to the hub."),
        status=404,
    )


def server_error(request):
    return _render_error(
        request,
        "500.html",
        code="500",
        title=_("Something went wrong"),
        message=_("We hit a snag on our side. Please try again in a moment."),
        status=500,
    )


def robots_txt(request):
    origin = (getattr(settings, "SITE_URL", "") or "").rstrip("/")
    if not origin:
        origin = f"{request.scheme}://{request.get_host()}"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /panel/",
        "Disallow: /api/",
        "Disallow: /api-auth/",
        "Disallow: /i18n/",
        "Disallow: /*/accounts/",
        "Disallow: /*/marketplace/new/",
        "Disallow: /*/marketplace/mine/",
        "Disallow: /*/marketplace/*/edit/",
        "Disallow: /*/marketplace/*/inquire/",
        "Disallow: /*/marketplace/*/sold/",
        "Disallow: /*/marketplace/*/withdraw/",
        "Disallow: /*/emergency/submit/",
        "Disallow: /*/emergency/*/verify/",
        "Disallow: /*/emergency/*/cancel/",
        "Disallow: /*/emergency/*/buzz/",
        "Disallow: /*/emergency/*/review/",
        "Disallow: /*/search/",
        "",
        f"Sitemap: {origin}/sitemap.xml",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
