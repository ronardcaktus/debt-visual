from django.db import models
from django.utils.translation import gettext_lazy as _

# Converts type floats to dollar ammounts
in_dollar = "${:,.2f}"


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
