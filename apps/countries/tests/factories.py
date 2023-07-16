
import factory

from apps.countries import models

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Country

    name = factory.Faker("country")
    population = factory.Faker("pyint")
    gdp = factory.Faker("pyint")
    internal_debt = factory.Faker("pyint")
    external_debt = factory.Faker("pyint")
