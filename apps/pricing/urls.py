from django.urls import path

from . import views

app_name = "pricing"

urlpatterns = [
    path("", views.list_prices, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
]
