from django.db import models

from apps.utils import (Continents, Regions, global_gdp, in_dollar,
                        world_population)


class Country(models.Model):
    name = models.CharField(max_length=200)
    flag = models.CharField(max_length=20)
    population = models.IntegerField()
    gdp = models.DecimalField(max_digits=100, decimal_places=2)
    internal_debt = models.DecimalField(max_digits=100, decimal_places=2)
    external_debt = models.DecimalField(max_digits=100, decimal_places=2)
    continent = models.CharField(
        max_length=max(len(x) for x in Continents.values),
        choices=Continents.choices,
        default="",
        blank=True,
    )
    region = models.CharField(
        max_length=max(len(x) for x in Regions.values),
        choices=Regions.choices,
        default="",
        blank=True,
    )
    source_link = models.URLField(max_length=300, blank=True, null=True)
    chart_link = models.URLField(max_length=300, blank=True, null=True)
    extra_link = models.URLField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ("pk",)

    def __str__(self):
        return f"{self.name}"

    @property
    def total_debt_as_int(self):
        return self.internal_debt + self.external_debt

    @property
    def total_debt(self):
        return in_dollar.format(self.internal_debt + self.external_debt)

    @property
    def internal_debt_per_citizen(self):
        return in_dollar.format(self.internal_debt / self.population)

    @property
    def external_debt_per_citizen(self):
        return in_dollar.format(self.external_debt / self.population)

    @property
    def total_debt_per_citizen(self):
        return in_dollar.format(self.total_debt_as_int / self.population)

    @property
    def debt_to_gpd_ratio(self):
        return in_dollar.format(self.total_debt_as_int / self.gdp)

    @property
    def population_percentage_of_the_world(self):
        country_vs_world_population = round(self.population / world_population, 4) * 100
        return f"{str(country_vs_world_population)}%"

    @property
    def gdp_as_percentage_of_global_gdp(self):
        return (self.gdp / global_gdp) * 100

    @property
    def gdp_as_percentage_of_region(self):
        countries_in_region = Country.objects.filter(region=self.region)
        total_region_gdp = sum(country.gdp for country in countries_in_region)
        country_gdp_region_percentage = (
            round((self.gdp / total_region_gdp) * 100, 4) if total_region_gdp else 0
        )
        return country_gdp_region_percentage
