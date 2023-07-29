import pytest
from django.test import TestCase

from apps.countries.tests.factories import CountryFactory
from apps.utils import dollar_format, global_gdp, world_population


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
        assert self.cf.total_debt == dollar_format.format(self.total_debt_as_int)

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


# result = CountryFactory.build(population=input_str).formatted_population
@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("123", "123"),
        ("1000", "1 thousand"),
        ("9999", "9.999 thousand"),
        ("10000", "10 thousand"),
        ("99999", "99.999 thousand"),
        ("100000", "100 thousand"),
        ("999999", "999.999 thousand"),
        ("1000000", "1.0 million"),
        ("9999999", "10.0 million"),
        ("10000000", "10.0 million"),
        ("99999999", "100.0 million"),
        ("100000000", "100.0 million"),
        ("999999999", "1.0 billion"),
        ("1000000000", "1.0 billion"),
        ("9999999999", "10.0 billion"),
        ("10000000000", "10.0 billion"),
        ("99999999999", "100.0 billion"),
        ("100000000000", "100.0 billion"),
        ("1234567890", "1.2 billion"),
        ("123456", "123.456 hundred"),
        ("1234567", "1.2 million"),
        ("1000000000000", "1,000.0 billion"),
    ],
)
def test_formatted_population(input_str, expected_output):
    result = CountryFactory.build(population=input_str).formatted_population
    assert (
        result == expected_output
    ), f"Error: Input: {input_str}, Expected: {expected_output}, Got: {result}"
