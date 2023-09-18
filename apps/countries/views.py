from django.shortcuts import render

from apps.countries.models import Country, GDPTrend


def index(request):
    return render(request, "country/index.html")


def country_detail(request, country_id):
    countries = Country.objects.filter(id=country_id)
    try:
        selected_country = countries[0]
        gdp_data = GDPTrend.objects.get(country=selected_country)
    except GDPTrend.DoesNotExist:
        gdp_data = None
    if gdp_data and gdp_data.gdp1 is not None:
        return render(
            request,
            "country/country_detail.html",
            {"countries": countries, "gdp_data": gdp_data},
        )
    return render(request, "country/country_detail.html", {"countries": countries})


def search_countries(request):
    countries = []
    search_keys = list(request.GET.keys())
    search_key = search_keys[0] if search_keys else None
    if search_key == "q":
        query = request.GET.get("q")
        if query:
            countries = Country.objects.filter(name__icontains=query)
        return render(request, "country/list.html", {"countries": countries})
    query = request.GET.get("q_comparison")
    if query:
        countries = Country.objects.filter(name__icontains=query)
    return render(request, "country/list_comparison.html", {"countries": countries})


def match_countries(request):
    return render(request, "country/match_countries.html")
