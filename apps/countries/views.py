from django.shortcuts import render

from apps.countries.models import Country, GDPTrend


def index(request):
    return render(request, "country/index.html")


def country_detail(request, country_id):
    countries = Country.objects.filter(id=country_id)
    try:
        selected_country = countries[0]
        country_has_gdp_data = GDPTrend.objects.get(country=selected_country)
    except GDPTrend.DoesNotExist:
        country_has_gdp_data = None
    if country_has_gdp_data and country_has_gdp_data.gdp1 is not None:
        return render(
            request,
            "country/country_detail.html",
            {"countries": countries, "country_has_gdp_data": country_has_gdp_data},
        )
    return render(request, "country/country_detail.html", {"countries": countries})


def search_countries(request):
    query = request.GET.get("q")
    countries = []
    if query:
        countries = Country.objects.filter(name__icontains=query)
    return render(request, "country/list.html", {"countries": countries})
