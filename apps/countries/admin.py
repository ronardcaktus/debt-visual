from django.contrib import admin

from apps.countries import models


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "region", "total_debt_in_dollars", "flag"]
    search_fields = ("name", "region", "continent")
    list_filter = ("continent", "region")
    ordering = ("-gdp",)


admin.site.register(models.Country, CountryAdmin)
