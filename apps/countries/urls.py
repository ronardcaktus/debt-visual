from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path(
        "countries-comparison/",
        views.match_countries,
        name="countries-comparison",
    ),
    path("search/", views.search_countries, name="search_countries"),
    path(
        "country-detail/<int:country_id>/", views.country_detail, name="country_details"
    ),
    path(
        "compare-country/<int:country_id>/",
        views.comparison_country_1,
        name="comparison_country_1",
    ),
    path(
        "compare-country-2/<int:country_id>/",
        views.comparison_country_2,
        name="comparison_country_2",
    ),
]
