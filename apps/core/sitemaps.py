"""Multilingual sitemaps for public indexable pages."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.cars.models import Car
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo


class I18nSitemap(Sitemap):
    """Base sitemap that emits fa/en/ar URLs with hreflang alternates."""

    i18n = True
    alternates = True
    # Avoid language-stripped x-default URLs (prefix_default_language=True).
    x_default = False


class StaticSectionSitemap(I18nSitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return [
            "core:home",
            "marketplace:list",
            "cars:list",
            "pricing:list",
            "stories:list",
            "youtube:list",
            "emergency:list",
        ]

    def location(self, item):
        return reverse(item)


class ListingSitemap(I18nSitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return (
            Listing.objects.filter(status=ListingStatus.ACTIVE)
            .order_by("-updated_at")
            .only("id", "updated_at")
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("marketplace:detail", kwargs={"pk": obj.pk})


class CarSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Car.objects.filter(is_published=True).order_by("-year", "id").only("id")

    def location(self, obj):
        return reverse("cars:detail", kwargs={"pk": obj.pk})


class PricingSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return (
            PriceReference.objects.filter(is_published=True)
            .order_by("-updated_at")
            .only("id", "updated_at")
        )

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("pricing:detail", kwargs={"pk": obj.pk})


class StorySitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return (
            Story.objects.filter(is_published=True)
            .order_by("-published_at", "-updated_at")
            .only("id", "slug", "published_at", "updated_at")
        )

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at

    def location(self, obj):
        return reverse("stories:detail", kwargs={"slug": obj.slug})


class YoutubeSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return (
            YoutubeVideo.objects.filter(is_published=True)
            .order_by("-published_at", "-created_at")
            .only("id", "published_at", "created_at")
        )

    def lastmod(self, obj):
        return obj.published_at or obj.created_at

    def location(self, obj):
        return reverse("youtube:detail", kwargs={"pk": obj.pk})


SITEMAPS = {
    "static": StaticSectionSitemap,
    "listings": ListingSitemap,
    "cars": CarSitemap,
    "pricing": PricingSitemap,
    "stories": StorySitemap,
    "youtube": YoutubeSitemap,
}
