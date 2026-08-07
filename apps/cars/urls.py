from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("", views.list_cars, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
]
