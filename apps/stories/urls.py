from django.urls import path

from . import views

app_name = "stories"

urlpatterns = [
    path("", views.list_stories, name="list"),
    path("<slug:slug>/", views.detail, name="detail"),
]
