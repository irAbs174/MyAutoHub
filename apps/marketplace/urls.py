from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.list_listings, name="list"),
    path("new/", views.create_listing, name="create"),
    path("mine/", views.my_listings, name="mine"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/edit/", views.edit_listing, name="edit"),
    path("<int:pk>/sold/", views.mark_sold, name="mark_sold"),
    path("<int:pk>/withdraw/", views.withdraw_listing, name="withdraw"),
    path("<int:pk>/inquire/", views.inquire, name="inquire"),
]
