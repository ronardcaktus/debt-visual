from django.db.models import Q
from django.shortcuts import render

from apps.countries.models import Country


def index(request):
    return render(request, "country/index.html")


def country_detail(request):
    query = request.GET.get("q")
    if not query:
        countries = ""
    countries = Country.objects.filter(Q(name__icontains=query))
    context = {
        "countries": countries,
    }
    return render(request, "country/country_detail.html", context)
