from django.contrib import admin

from apps.countries import models


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "gdp_in_dollars", "total_debt_in_dollars", "flag"]
    search_fields = ("name", "region", "continent")
    list_filter = ("continent", "region")
    ordering = ("-gdp",)


class GPDTrendAdmin(admin.ModelAdmin):
    list_display = ["country", "gdp1", "gdp2", "gdp3", "gdp13", "gdp14", "gdp15"]


admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.GDPTrend, GPDTrendAdmin)
