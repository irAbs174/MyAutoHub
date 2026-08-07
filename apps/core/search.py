from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.cars.models import Car
from apps.core.i18n_content import localized
from apps.emergency.models import EmergencyService
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

SEARCH_LIMIT = 8
SUGGEST_LIMIT = 8
SUGGEST_PER_TYPE = 2


def run_search(q, *, limit=SEARCH_LIMIT):
    """Return categorized match lists for a query string."""
    q = (q or "").strip()
    empty = {
        "cars": [],
        "listings": [],
        "stories": [],
        "videos": [],
        "prices": [],
        "services": [],
    }
    if not q:
        return empty

    return {
        "cars": list(
            Car.objects.filter(is_published=True)
            .filter(
                Q(model__name__icontains=q)
                | Q(model__brand__name__icontains=q)
                | Q(trim__name__icontains=q)
                | Q(fuel_type__icontains=q)
                | Q(description__icontains=q)
            )
            .select_related("model__brand", "trim")
            .prefetch_related("photos")[:limit]
        ),
        "listings": list(
            Listing.objects.filter(status=ListingStatus.ACTIVE)
            .filter(
                Q(title_fa__icontains=q)
                | Q(title_en__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(description_fa__icontains=q)
                | Q(description_en__icontains=q)
                | Q(description_ar__icontains=q)
                | Q(city__icontains=q)
            )
            .select_related("seller")
            .prefetch_related("photos")[:limit]
        ),
        "stories": list(
            Story.objects.filter(is_published=True)
            .filter(
                Q(title_fa__icontains=q)
                | Q(title_en__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(excerpt_fa__icontains=q)
                | Q(excerpt_en__icontains=q)
                | Q(excerpt_ar__icontains=q)
                | Q(body_fa__icontains=q)
                | Q(body_en__icontains=q)
                | Q(body_ar__icontains=q)
            )
            .select_related("author")[:limit]
        ),
        "videos": list(
            YoutubeVideo.objects.filter(is_published=True)
            .filter(Q(title__icontains=q) | Q(description__icontains=q))[:limit]
        ),
        "prices": list(
            PriceReference.objects.filter(is_published=True)
            .filter(
                Q(title_fa__icontains=q)
                | Q(title_en__icontains=q)
                | Q(title_ar__icontains=q)
                | Q(category_fa__icontains=q)
                | Q(category_en__icontains=q)
                | Q(category_ar__icontains=q)
                | Q(notes_fa__icontains=q)
                | Q(notes_en__icontains=q)
                | Q(notes_ar__icontains=q)
                | Q(source_fa__icontains=q)
                | Q(source_en__icontains=q)
                | Q(source_ar__icontains=q)
            )
            .prefetch_related("photos")[:limit]
        ),
        "services": list(
            EmergencyService.objects.filter(is_active=True)
            .filter(
                Q(name_fa__icontains=q)
                | Q(name_en__icontains=q)
                | Q(name_ar__icontains=q)
                | Q(description_fa__icontains=q)
                | Q(description_en__icontains=q)
                | Q(description_ar__icontains=q)
                | Q(coverage_notes_fa__icontains=q)
                | Q(coverage_notes_en__icontains=q)
                | Q(coverage_notes_ar__icontains=q)
            )[:limit]
        ),
    }


def _join_meta(*parts):
    return " · ".join(str(p) for p in parts if p)


def build_suggest_results(q, *, request=None, limit=SUGGEST_LIMIT):
    """Flat typeahead rows matching landing search (category / title / subtitle)."""
    q = (q or "").strip()
    if not q:
        return []

    buckets = run_search(q, limit=SUGGEST_PER_TYPE)
    results = []

    for car in buckets["cars"]:
        results.append(
            {
                "id": f"car:{car.pk}",
                "category": "car",
                "category_label": _("Car"),
                "title": f"{car.model.brand.name} {car.model.name}",
                "subtitle": _join_meta(
                    car.year, car.trim.name if car.trim_id else None
                ),
                "url": reverse("cars:detail", args=[car.pk]),
            }
        )

    for item in buckets["listings"]:
        try:
            price = f"{int(item.price):,} {item.currency}"
        except (TypeError, ValueError):
            price = f"{item.price} {item.currency}"
        results.append(
            {
                "id": f"listing:{item.pk}",
                "category": "listing",
                "category_label": _("Marketplace"),
                "title": localized(item, "title"),
                "subtitle": _join_meta(item.city, item.year, price),
                "url": reverse("marketplace:detail", args=[item.pk]),
            }
        )

    for story in buckets["stories"]:
        author = ""
        if story.author_id:
            author = story.author.get_username()
        results.append(
            {
                "id": f"story:{story.pk}",
                "category": "story",
                "category_label": _("Story"),
                "title": localized(story, "title"),
                "subtitle": localized(story, "excerpt") or author,
                "url": reverse("stories:detail", args=[story.slug]),
            }
        )

    for video in buckets["videos"]:
        desc = (video.description or "").strip()
        results.append(
            {
                "id": f"video:{video.pk}",
                "category": "video",
                "category_label": _("Video"),
                "title": video.title,
                "subtitle": (desc[:80] + ("…" if len(desc) > 80 else "")) if desc else "",
                "url": reverse("youtube:detail", args=[video.pk]),
            }
        )

    for price in buckets["prices"]:
        try:
            amount = f"{int(price.amount):,} {price.currency}"
        except (TypeError, ValueError):
            amount = f"{price.amount} {price.currency}"
        results.append(
            {
                "id": f"price:{price.pk}",
                "category": "price",
                "category_label": _("Pricing"),
                "title": localized(price, "title"),
                "subtitle": _join_meta(localized(price, "category"), amount),
                "url": reverse("pricing:detail", args=[price.pk]),
            }
        )

    emergency_url = reverse("emergency:submit")
    if request is not None and not request.user.is_authenticated:
        emergency_url = f"{reverse('accounts:login')}?next={emergency_url}"

    for svc in buckets["services"]:
        desc = localized(svc, "description") or _("Roadside help")
        results.append(
            {
                "id": f"emergency:{svc.pk}",
                "category": "emergency",
                "category_label": _("Emergency"),
                "title": localized(svc, "name"),
                "subtitle": desc[:100],
                "url": emergency_url,
            }
        )

    return results[:limit]
