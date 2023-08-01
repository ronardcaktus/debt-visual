from decimal import Decimal

import pytest
from django.test import TestCase

from apps.countries.tests.factories import CountryFactory
from apps.utils import (dollar_format, format_country_or_continent, global_gdp,
                        limit_2_decimals, world_population)


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
        assert f"{self.cf.total_debt_in_dollars}.00" == dollar_format.format(
            self.total_debt_as_int
        )

    def test_internal_debt_per_citizen(self):
        internal_debt = self.internal_debt / self.population
        assert self.cf.internal_debt_per_citizen == dollar_format.format(internal_debt)

    def test_external_debt_per_citizen(self):
        ext_debt_per_citizen = self.external_debt / self.population
        assert self.cf.external_debt_per_citizen == dollar_format.format(
            ext_debt_per_citizen
        )

    def test_total_debt_per_citizen(self):
        total_debt_per_citizen = self.total_debt_as_int / self.population
        assert self.cf.total_debt_per_citizen == dollar_format.format(
            total_debt_per_citizen
        )

    def test_debt_to_gpd_ratio(self):
        debt_to_gpd_ratio = self.total_debt_as_int / self.gdp
        assert self.cf.debt_to_gpd_ratio == dollar_format.format(debt_to_gpd_ratio)

    def test_population_percentage_of_the_world(self):
        country_vs_world_population = round(self.population / world_population, 4) * 100
        assert (
            self.cf.population_percentage_of_the_world
            == f"{str(country_vs_world_population)}%"
        )

    def test_gdp_as_percentage_of_global_gdp(self):
        assert self.cf.gdp_as_percentage_of_global_gdp == (self.gdp / global_gdp) * 100

    def test_continent_formatted(self):
        assert self.cf.continent != self.cf.continent_formatted
        assert self.cf.continent_formatted == format_country_or_continent(
            self.cf.continent
        )

    def test_region_formatted(self):
        assert self.cf.region != self.cf.region_formatted
        assert self.cf.region_formatted == format_country_or_continent(self.cf.region)


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
        assert Decimal(country.gdp_as_percentage_of_region) == Decimal(
            limit_2_decimals.format(expected_percentage)
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
        assert Decimal(country.gdp_as_percentage_of_region) == Decimal(
            limit_2_decimals.format(expected_percentage)
        )

    def test_gdp_as_percentage_of_region_ensure_returns_zero(self):
        region_countries = CountryFactory.create_batch(3, region=self.region, gdp=0)
        country = CountryFactory(region=self.region, gdp=0)
        total_region_gdp = sum(country.gdp for country in region_countries)
        expected_percentage = (
            (country.gdp / total_region_gdp) * 100 if total_region_gdp != 0 else 0
        )
        assert (
            int(country.gdp_as_percentage_of_region) == 0 and expected_percentage == 0
        )


# Tests formatted_population property in Country model
@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("1000000", "1.0 million"),
        ("9999999", "10.0 million"),
        ("10000000", "10.0 million"),
        ("99999999", "100.0 million"),
        ("100000000", "100.0 million"),
        # Edgecase - 999 million, 999 thousand, and 999
        # shows as 1,000.0 million because they aren't one
        # billion.
        ("999999999", "1,000.0 million"),
        ("1000000000", "1.0 billion"),
        ("9999999999", "10.0 billion"),
        ("10000000000", "10.0 billion"),
        ("99999999999", "100.0 billion"),
        ("100000000000", "100.0 billion"),
        ("1234567890", "1.2 billion"),
        ("123456", "123.5 thousand"),
        ("1234567", "1.2 million"),
        ("1000000000000", "1.0 trillion"),
    ],
)
def test_formatted_population(input_str, expected_output):
    result = CountryFactory.build(population=input_str).formatted_population
    assert (
        result == expected_output
    ), f"Error: Input: {input_str}, Expected: {expected_output}, Got: {result}"
