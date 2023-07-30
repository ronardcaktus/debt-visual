from django.db import models
from numerize import numerize

from apps import utils


class Country(models.Model):
    name = models.CharField(max_length=200)
    flag = models.CharField(max_length=20)
    population = models.IntegerField()
    gdp = models.DecimalField(max_digits=100, decimal_places=2)
    internal_debt = models.DecimalField(max_digits=100, decimal_places=2)
    external_debt = models.DecimalField(max_digits=100, decimal_places=2)
    continent = models.CharField(
        max_length=max(len(x) for x in utils.Continents.values),
        choices=utils.Continents.choices,
        default="",
        blank=True,
    )
    region = models.CharField(
        max_length=max(len(x) for x in utils.Regions.values),
        choices=utils.Regions.choices,
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
    def gdp_in_dollars(self):
        return f"${numerize.numerize(self.gdp, 4)}"

    @property
    def int_debt_in_dollars(self):
        return f"${numerize.numerize(self.internal_debt)}"

    @property
    def ext_debt_in_dollars(self):
        return f"${numerize.numerize(self.external_debt)}"

    @property
    def total_debt_in_dollars(self):
        return f"${numerize.numerize(self.internal_debt + self.external_debt)}"

    @property
    def formatted_population(self):
        # For now I am OK with using round and therefore
        # rounding up, since population is increasingly growing.
        population_number = int(self.population)
        suffix = ""

        if population_number >= 1_000_000_000_000:
            suffix = " trillion"
            formatted_population = utils.population_format.format(
                round(population_number / 1_000_000_000_000, 1)
            )
        elif population_number >= 1_000_000_000:
            suffix = " billion"
            formatted_population = utils.population_format.format(
                round(population_number / 1_000_000_000, 1)
            )
        elif population_number >= 1_000_000:
            suffix = " million"
            formatted_population = utils.population_format.format(
                round(population_number / 1_000_000, 1)
            )
        elif population_number >= 1_000:
            suffix = " thousand"
            formatted_population = utils.population_format.format(
                round(population_number / 1_000, 1)
            )
        else:
            formatted_population = utils.population_format.format(population_number)

        return f"{formatted_population}{suffix}"

    @property
    def internal_debt_per_citizen(self):
        return utils.dollar_format.format(self.internal_debt / self.population)

    @property
    def external_debt_per_citizen(self):
        return utils.dollar_format.format(self.external_debt / self.population)

    @property
    def total_debt_per_citizen(self):
        return utils.dollar_format.format(self.total_debt_as_int / self.population)

    @property
    def debt_to_gpd_ratio(self):
        return utils.dollar_format.format(self.total_debt_as_int / self.gdp)

    @property
    def population_percentage_of_the_world(self):
        country_vs_world_population = (
            round(self.population / utils.world_population, 4) * 100
        )
        return f"{str(country_vs_world_population)}%"

    @property
    def gdp_as_percentage_of_global_gdp(self):
        return (self.gdp / utils.global_gdp) * 100

    @property
    def gdp_as_percentage_of_region(self):
        countries_in_region = Country.objects.filter(region=self.region)
        total_region_gdp = sum(country.gdp for country in countries_in_region)
        country_gdp_region_percentage = (
            round((self.gdp / total_region_gdp) * 100, 4) if total_region_gdp else 0
        )
        return country_gdp_region_percentage

    @property
    def continent_formatted(self):
        return utils.format_country_or_continent(self.continent)

    @property
    def region_formatted(self):
        return utils.format_country_or_continent(self.region)
