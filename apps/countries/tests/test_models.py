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
        internal_debt = round(self.internal_debt / self.population, 2)
        assert self.cf.internal_debt_per_citizen == internal_debt

    def test_external_debt_per_citizen(self):
        ext_debt_per_citizen = round(self.external_debt / self.population, 2)
        assert self.cf.external_debt_per_citizen == ext_debt_per_citizen

    def test_total_debt_per_citizen(self):
        total_debt_per_citizen = round(self.total_debt_as_int / self.population, 2)
        assert self.cf.total_debt_per_citizen == round(total_debt_per_citizen, 2)

    def test_debt_to_gpd_ratio(self):
        debt_to_gpd_ratio = round((self.total_debt_as_int / self.gdp), 2)
        assert self.cf.debt_to_gpd_ratio == debt_to_gpd_ratio

    def test_gdp_per_capita(self):
        gdp_per_capita = round(self.gdp / self.population, 2)
        assert self.cf.gdp_per_capita == gdp_per_capita

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
        ("9999999", "9.9 million"),
        ("10000000", "10.0 million"),
        ("99999999", "99.9 million"),
        ("100000000", "100.0 million"),
        ("999999999", "999.9 million"),
        ("1000000000", "1.0 billion"),
        ("9999999999", "9.9 billion"),
        ("10000000000", "10.0 billion"),
        ("99999999999", "99.9 billion"),
        ("100000000000", "100.0 billion"),
        ("1234567890", "1.2 billion"),
        ("123456", "123.4 thousand"),
        ("1234567", "1.2 million"),
        ("1000000000000", "1.0 trillion"),
        ("1999999999999", "1.9 trillion"),
    ],
)
def test_formatted_population(input_str, expected_output):
    result = CountryFactory.build(population=input_str).formatted_population
    assert (
        result == expected_output
    ), f"Error: Input: {input_str}, Expected: {expected_output}, Got: {result}"
