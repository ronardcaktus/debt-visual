from decimal import ROUND_DOWN, Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

# Converts type floats to dollar ammounts
dollar_format = "${:,.2f}"
# Converts string to population
population_format = "{:,}"
# Limits to two decimal places
limit_2_decimals = "{:.2f}"

world_population = int(8044465170)

global_gdp = 96510000000000  # as of 2021


class Continents(models.TextChoices):
    ASIA = "asia", _("Asia")
    AFRICA = "africa", _("Africa")
    NORTH_AMERICA = "north_america", _("North America")
    SOUTH_AMERICA = "south_america", _("South America")
    EUROPE = "europe", _("Europe")
    AUSTRALIA = "australia", _("Australia")


class Regions(models.TextChoices):
    ASIA = "asia", _("Asia")
    AFRICA = "africa", _("Africa")
    NORTH_AMERICA = "north_america", _("North America")
    SOUTH_AMERICA = "south_america", _("South America")
    EUROPE = "europe", _("Europe")
    AUSTRALIA = "australia", _("Australia")
    CARIBBEAN = "caribbean", _("Caribbean")
    CENTRAL_AMERICA = "central_america", _("Central America")
    OCEANIA = "oceania", _("Oceania")


def format_country_or_continent(name):
    """
    Intakes a str(country or continent) in cammel case: 'north_america'
    and replaces the _ with spaces and capitalizes the first letter.
    Returning 'North America'.
    """
    formatted_name = " ".join(word.capitalize() for word in name.split("_"))
    return formatted_name


def rounds_numbers_accurately(number):
    """Accurately trims float to 1 decimal without rounding."""
    rounded_number = Decimal(str(number)).quantize(Decimal("0.1"), rounding=ROUND_DOWN)
    return float(rounded_number)
