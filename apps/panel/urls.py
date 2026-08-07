from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("emergency/", views.emergency_request_list, name="emergency_request_list"),
    path(
        "emergency/services/",
        views.emergency_service_list,
        name="emergency_service_list",
    ),
    path(
        "emergency/services/new/",
        views.emergency_service_create,
        name="emergency_service_create",
    ),
    path(
        "emergency/services/<int:pk>/edit/",
        views.emergency_service_edit,
        name="emergency_service_edit",
    ),
    path(
        "emergency/<int:pk>/",
        views.emergency_request_detail,
        name="emergency_request_detail",
    ),
    path(
        "emergency/<int:pk>/verify/",
        views.emergency_request_verify,
        name="emergency_request_verify",
    ),
    path("cars/", views.car_list, name="car_list"),
    path("cars/new/", views.car_create, name="car_create"),
    path("cars/<int:pk>/edit/", views.car_edit, name="car_edit"),
    path("cars/brands/", views.brand_list, name="brand_list"),
    path("cars/brands/new/", views.brand_create, name="brand_create"),
    path("cars/brands/<int:pk>/edit/", views.brand_edit, name="brand_edit"),
    path("cars/models/new/", views.car_model_create, name="car_model_create"),
    path("cars/models/<int:pk>/edit/", views.car_model_edit, name="car_model_edit"),
    path("youtube/", views.youtube_list, name="youtube_list"),
    path("youtube/new/", views.youtube_create, name="youtube_create"),
    path("youtube/<int:pk>/edit/", views.youtube_edit, name="youtube_edit"),
    path("stories/", views.story_list, name="story_list"),
    path("stories/new/", views.story_create, name="story_create"),
    path("stories/<int:pk>/edit/", views.story_edit, name="story_edit"),
]
