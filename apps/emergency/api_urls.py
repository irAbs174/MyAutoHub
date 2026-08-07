from django.urls import path

from . import api_views

urlpatterns = [
    path("submit/", api_views.SubmitEmergencyRequestAPIView.as_view(), name="api_submit"),
    path("search/", api_views.SearchEmergencyAPIView.as_view(), name="api_search"),
    path(
        "<int:pk>/verify/",
        api_views.VerifyEmergencyAPIView.as_view(),
        name="api_verify",
    ),
    path(
        "<int:pk>/cancel/",
        api_views.CancelEmergencyAPIView.as_view(),
        name="api_cancel",
    ),
    path("<int:pk>/buzz/", api_views.BuzzEmergencyAPIView.as_view(), name="api_buzz"),
    path(
        "<int:pk>/review/",
        api_views.ReviewEmergencyAPIView.as_view(),
        name="api_review",
    ),
]
