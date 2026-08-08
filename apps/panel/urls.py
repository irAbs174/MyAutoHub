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
    path("cars/categories/", views.category_list, name="category_list"),
    path("cars/categories/new/", views.category_create, name="category_create"),
    path(
        "cars/categories/<int:pk>/edit/",
        views.category_edit,
        name="category_edit",
    ),
    path("cars/models/new/", views.car_model_create, name="car_model_create"),    path("cars/models/<int:pk>/edit/", views.car_model_edit, name="car_model_edit"),
    path("cars/trims/new/", views.trim_create, name="trim_create"),
    path("cars/trims/<int:pk>/edit/", views.trim_edit, name="trim_edit"),
    path("cars/obd/", views.obd_list, name="obd_list"),
    path("cars/obd/new/", views.obd_create, name="obd_create"),
    path("cars/obd/<int:pk>/edit/", views.obd_edit, name="obd_edit"),
    path("dealers/", views.dealer_list, name="dealer_list"),
    path("dealers/new/", views.dealer_create, name="dealer_create"),
    path("dealers/<int:pk>/edit/", views.dealer_edit, name="dealer_edit"),
    path("repair-shops/", views.repair_shop_list, name="repair_shop_list"),
    path("repair-shops/new/", views.repair_shop_create, name="repair_shop_create"),
    path(
        "repair-shops/<int:pk>/edit/",
        views.repair_shop_edit,
        name="repair_shop_edit",
    ),
    path("youtube/", views.youtube_list, name="youtube_list"),
    path("youtube/new/", views.youtube_create, name="youtube_create"),
    path("youtube/<int:pk>/edit/", views.youtube_edit, name="youtube_edit"),
    path("stories/", views.story_list, name="story_list"),
    path("stories/new/", views.story_create, name="story_create"),
    path("stories/<int:pk>/edit/", views.story_edit, name="story_edit"),
    path("marketplace/", views.listing_list, name="listing_list"),
    path("marketplace/new/", views.listing_create, name="listing_create"),
    path("marketplace/<int:pk>/edit/", views.listing_edit, name="listing_edit"),
    path("marketplace/inquiries/", views.inquiry_list, name="inquiry_list"),
    path("pricing/", views.price_list, name="price_list"),
    path("pricing/new/", views.price_create, name="price_create"),
    path("pricing/<int:pk>/edit/", views.price_edit, name="price_edit"),
]
