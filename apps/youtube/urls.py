from django.urls import path

from . import views

app_name = "youtube"

urlpatterns = [
    path("", views.list_videos, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
]
