from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search/", views.search_countries, name="search_countries"),
    path("country-detail/<int:country_id>/", views.country_detail, name="country_details"),
]
