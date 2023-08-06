from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("country-detail", views.country_detail, name="country_details"),
]
