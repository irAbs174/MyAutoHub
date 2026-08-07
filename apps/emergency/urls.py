from django.urls import path

from . import views

app_name = "emergency"

urlpatterns = [
    path("", views.list_requests, name="list"),
    path("submit/", views.submit_request, name="submit"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/verify/", views.verify, name="verify"),
    path("<int:pk>/cancel/", views.cancel, name="cancel"),
    path("<int:pk>/buzz/", views.buzz, name="buzz"),
    path("<int:pk>/review/", views.review, name="review"),
]
