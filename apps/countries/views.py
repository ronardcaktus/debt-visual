from django.shortcuts import render

from apps.countries.models import Country


def index(request):
    return render(request, "country/index.html")


def country_detail(request, country_id):
    countries = Country.objects.filter(id=country_id)
    return render(request, "country/country_detail.html", {"countries": countries})


def search_countries(request):
    query = request.GET.get("q")
    countries = []
    if query:
        countries = Country.objects.filter(name__icontains=query)
    return render(request, "country/list.html", {"countries": countries})
