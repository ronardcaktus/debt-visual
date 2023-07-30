from django.shortcuts import render

from apps.countries.models import Country


def country_detail(request):
    countries = Country.objects.filter(id="1")
    context = {
        "countries": countries,
    }
    return render(request, "country/country_detail.html", context)
