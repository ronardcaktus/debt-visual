from django.test import TestCase

from apps.countries.tests.factories import CountryFactory
from apps.utils import global_gdp, in_dollar, world_population


class TestCountryProperties:
    internal_debt = 100
    external_debt = 100
    population = 80
    gdp = 150
    total_debt_as_int = internal_debt + external_debt
    cf = CountryFactory.build(
        internal_debt=internal_debt,
        external_debt=external_debt,
        population=population,
        gdp=gdp,
    )

    def test_total_debt(self):
        assert self.cf.total_debt == in_dollar.format(self.total_debt_as_int)

    def test_internal_debt_per_citizen(self):
        internal_debt = self.internal_debt / self.population
        assert self.cf.internal_debt_per_citizen == in_dollar.format(internal_debt)

    def test_external_debt_per_citizen(self):
        ext_debt_per_citizen = self.external_debt / self.population
        assert self.cf.external_debt_per_citizen == in_dollar.format(
            ext_debt_per_citizen
        )

    def test_total_debt_per_citizen(self):
        total_debt_per_citizen = self.total_debt_as_int / self.population
        assert self.cf.total_debt_per_citizen == in_dollar.format(
            total_debt_per_citizen
        )

    def test_debt_to_gpd_ratio(self):
        debt_to_gpd_ratio = self.total_debt_as_int / self.gdp
        assert self.cf.debt_to_gpd_ratio == in_dollar.format(debt_to_gpd_ratio)

    def test_population_percentage_of_the_world(self):
        country_vs_world_population = round(self.population / world_population, 4) * 100
        assert (
            self.cf.population_percentage_of_the_world
            == f"{str(country_vs_world_population)}%"
        )

    def test_gdp_as_percentage_of_global_gdp(self):
        assert self.cf.gdp_as_percentage_of_global_gdp == (self.gdp / global_gdp) * 100


class CountryModelTests(TestCase):
    region = "Europe"

    def test_gdp_as_percentage_of_region(self):
        region_countries = CountryFactory.create_batch(5, region=self.region)
        country = CountryFactory(region=self.region)

        # Calculate the total GDP of countries in the same region, including the current country
        total_region_gdp = (
            sum(country.gdp for country in region_countries) + country.gdp
        )

        # Expected GDP percentage
        expected_percentage = (
            (country.gdp / total_region_gdp) * 100 if total_region_gdp != 0 else 0
        )

        assert round(country.gdp_as_percentage_of_region, 4) == round(
            expected_percentage, 4
        )

    def test_gdp_as_percentage_of_region_countries_gpd_zero(self):
        region_countries = CountryFactory.create_batch(5, region=self.region)
        country = CountryFactory(region=self.region)

        # Add countries with GDP = 0 to the region
        zero_gdp_country = CountryFactory(region=self.region, gdp=0)
        another_zero_gdp_country = CountryFactory(region=self.region, gdp=0)

        total_region_gdp = (
            sum(country.gdp for country in region_countries)
            + country.gdp
            + zero_gdp_country.gdp
            + another_zero_gdp_country.gdp
        )
        expected_percentage = (
            (country.gdp / total_region_gdp) * 100 if total_region_gdp != 0 else 0
        )
        assert round(country.gdp_as_percentage_of_region, 4) == round(
            expected_percentage, 4
        )

    def test_gdp_as_percentage_of_region_ensure_returns_zero(self):
        region_countries = CountryFactory.create_batch(3, region=self.region, gdp=0)
        country = CountryFactory(region=self.region, gdp=0)
        total_region_gdp = sum(country.gdp for country in region_countries)
        expected_percentage = (
            (country.gdp / total_region_gdp) * 100 if total_region_gdp != 0 else 0
        )
        assert (
            round(country.gdp_as_percentage_of_region, 4) == 0
            and expected_percentage == 0
        )
