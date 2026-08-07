from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("", views.list_cars, name="list"),
    path("brands/", views.brand_list, name="brands"),
    path("brands/<int:pk>/", views.brand_detail, name="brand_detail"),
    path("<int:pk>/", views.detail, name="detail"),
]
