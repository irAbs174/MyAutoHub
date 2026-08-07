from django.urls import path

from . import api_views

urlpatterns = [
    path("hub/", api_views.PublicHubAPIView.as_view(), name="public_hub"),
    path("cars/", api_views.PublicCarsAPIView.as_view(), name="public_cars"),
    path(
        "cars/<int:pk>/",
        api_views.PublicCarDetailAPIView.as_view(),
        name="public_car_detail",
    ),
    path("dealers/", api_views.PublicDealersAPIView.as_view(), name="public_dealers"),
    path(
        "repair-shops/",
        api_views.PublicRepairShopsAPIView.as_view(),
        name="public_repair_shops",
    ),
    path(
        "search/",
        api_views.PublicSearchSuggestAPIView.as_view(),
        name="public_search_suggest",
    ),
]
