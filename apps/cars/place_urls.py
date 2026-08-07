from django.urls import path

from apps.cars import views

app_name = "places"

urlpatterns = [
    path("", views.places_index, name="index"),
    path("dealers/<int:pk>/", views.dealer_detail, name="dealer_detail"),
    path(
        "repair-shops/<int:pk>/",
        views.repair_shop_detail,
        name="repair_shop_detail",
    ),
]
