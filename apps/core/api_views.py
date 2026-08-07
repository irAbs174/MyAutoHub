from django.conf import settings
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.models import Brand, Car, Dealer, RepairShop
from apps.emergency.models import EmergencyService
from apps.marketplace.models import Listing, ListingStatus
from apps.pricing.models import PriceReference
from apps.stories.models import Story
from apps.youtube.models import YoutubeVideo

from .api_serializers import (
    BrandSerializer,
    DealerSerializer,
    PublicCarDetailSerializer,
    PublicCarSerializer,
    PublicEmergencyServiceSerializer,
    PublicListingSerializer,
    PublicPriceReferenceSerializer,
    PublicStorySerializer,
    PublicYoutubeVideoSerializer,
    RepairShopSerializer,
)
from .search import build_suggest_results


class PublicCarsPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicHubAPIView(APIView):
    """Aggregated marketing teasers for the landing SPA (mirrors core.home)."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        ctx = {"request": request}
        cars = (
            Car.objects.filter(is_published=True)
            .select_related("model__brand", "trim")
            .prefetch_related("photos")[:6]
        )
        listings = (
            Listing.objects.filter(status=ListingStatus.ACTIVE)
            .select_related("seller", "car_model__brand")
            .prefetch_related("photos")[:4]
        )
        videos = YoutubeVideo.objects.filter(is_published=True)[:4]
        stories = Story.objects.filter(is_published=True).select_related("author")[:3]
        prices = (
            PriceReference.objects.filter(is_published=True).prefetch_related("photos")[:4]
        )
        emergency_services = EmergencyService.objects.filter(is_active=True)[:4]
        brands = Brand.objects.all()[:40]

        social_links = getattr(settings, "SOCIAL_LINKS", [])

        return Response(
            {
                "cars": PublicCarSerializer(cars, many=True, context=ctx).data,
                "listings": PublicListingSerializer(
                    listings, many=True, context=ctx
                ).data,
                "videos": PublicYoutubeVideoSerializer(
                    videos, many=True, context=ctx
                ).data,
                "stories": PublicStorySerializer(
                    stories, many=True, context=ctx
                ).data,
                "prices": PublicPriceReferenceSerializer(
                    prices, many=True, context=ctx
                ).data,
                "emergency_services": PublicEmergencyServiceSerializer(
                    emergency_services, many=True, context=ctx
                ).data,
                "brands": BrandSerializer(brands, many=True).data,
                "social_links": social_links,
            }
        )


class PublicCarsAPIView(ListAPIView):
    """Published car catalog for landing Quick View."""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = PublicCarSerializer
    pagination_class = PublicCarsPagination
    filterset_fields = []
    search_fields = ["model__name", "trim__name", "model__brand__name"]
    ordering_fields = ["year", "horsepower", "model__name", "model__brand__name"]
    ordering = ["-year", "model__brand__name", "model__name"]

    def get_queryset(self):
        qs = (
            Car.objects.filter(is_published=True)
            .select_related("model__brand", "trim")
            .prefetch_related("photos")
        )
        brand = self.request.query_params.get("brand")
        if brand:
            if brand.isdigit():
                qs = qs.filter(model__brand_id=int(brand))
            else:
                qs = qs.filter(model__brand__name__iexact=brand)

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(model__name__icontains=search)
                | Q(trim__name__icontains=search)
                | Q(model__brand__name__icontains=search)
            )

        fuel = self.request.query_params.get("fuel")
        if fuel:
            qs = qs.filter(fuel_type__iexact=fuel)

        year_min = self.request.query_params.get("year_min")
        if year_min and year_min.isdigit():
            qs = qs.filter(year__gte=int(year_min))

        year_max = self.request.query_params.get("year_max")
        if year_max and year_max.isdigit():
            qs = qs.filter(year__lte=int(year_max))

        return qs


class PublicCarDetailAPIView(RetrieveAPIView):
    """Full published car catalog entry with related catalog data."""

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = PublicCarDetailSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return (
            Car.objects.filter(is_published=True)
            .select_related(
                "model__brand",
                "trim",
                "technical_spec",
                "dimensions",
            )
            .prefetch_related(
                "photos",
                "features",
                "maintenance_items",
                "fluids",
                "tires",
                "batteries",
                "service_schedule",
                "parts",
                "prices",
                "model__obd_codes",
            )
        )


class PublicDealersAPIView(ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = DealerSerializer
    pagination_class = PublicCarsPagination

    def get_queryset(self):
        qs = Dealer.objects.filter(is_published=True).prefetch_related("brands")
        brand = self.request.query_params.get("brand")
        if brand:
            if brand.isdigit():
                qs = qs.filter(brands__id=int(brand))
            else:
                qs = qs.filter(brands__name__iexact=brand)
            qs = qs.distinct()
        return qs


class PublicRepairShopsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = RepairShopSerializer
    pagination_class = PublicCarsPagination

    def get_queryset(self):
        qs = RepairShop.objects.filter(is_published=True).prefetch_related("brands")
        brand = self.request.query_params.get("brand")
        if brand:
            if brand.isdigit():
                qs = qs.filter(brands__id=int(brand))
            else:
                qs = qs.filter(brands__name__iexact=brand)
            qs = qs.distinct()
        return qs


class PublicSearchSuggestAPIView(APIView):
    """Flat typeahead rows for the application nav search (landing-style list)."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        return Response(
            {
                "q": q,
                "results": build_suggest_results(q, request=request),
            }
        )
