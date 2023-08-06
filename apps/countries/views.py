from django.db.models import Q
from django.shortcuts import render

from apps.countries.models import Country


def index(request):
    return render(request, "country/index.html")


def country_detail(request):
    query = request.GET.get("q")
    if query:
        countries = Country.objects.filter(Q(name__icontains=query))
        context = {"countries": countries, "query": query}
        if countries.exists():
            return render(request, "country/country_detail.html", context)
        else:
            return render(request, "country/country_not_found.html", context)
