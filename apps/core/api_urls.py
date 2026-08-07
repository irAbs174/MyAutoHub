from django.urls import path

from . import api_views

urlpatterns = [
    path("hub/", api_views.PublicHubAPIView.as_view(), name="public_hub"),
    path("cars/", api_views.PublicCarsAPIView.as_view(), name="public_cars"),
    path(
        "search/",
        api_views.PublicSearchSuggestAPIView.as_view(),
        name="public_search_suggest",
    ),
]
