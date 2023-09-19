from django.shortcuts import get_object_or_404, render

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
    # I resisted creating two templates, one for each country's autocomplete
    # results, but I could not get the alignment to work solely by passing
    # a variable and using a conditional.
    elif search_key == "q_country_1":
        query = request.GET.get("q_country_1")
        if query:
            countries = Country.objects.filter(name__icontains=query)
        return render(
            request,
            "country/autocomplete_country_1.html",
            {"countries": countries},
        )
    else:
        query = request.GET.get("q_country_2")
        if query:
            countries = Country.objects.filter(name__icontains=query)
        return render(
            request,
            "country/autocomplete_country_2.html",
            {"countries": countries},
        )


def match_countries(request):
    return render(request, "country/match_countries.html")


def comparison_country_1(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    request.session["debt_to_gdp_ratio"] = str(country.debt_to_gpd_ratio)
    return render(request, "country/display_country_1.html", {"country": country})


def comparison_country_2(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    country_1_debt_to_gdp_ratio = (
        request.session.get("debt_to_gdp_ratio")
        if request.session.get("debt_to_gdp_ratio")
        else None
    )
    print(country_1_debt_to_gdp_ratio)  # TODO: Delete me later
    return render(request, "country/display_country_2.html", {"country": country})
