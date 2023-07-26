import factory

from apps.countries import models


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Country

    name = factory.Faker("country")
    population = factory.Faker("pyint")
    gdp = factory.Faker("pydecimal", left_digits=10, right_digits=2, positive=True)
    internal_debt = factory.Faker(
        "pydecimal", left_digits=10, right_digits=2, positive=True
    )
    external_debt = factory.Faker(
        "pydecimal", left_digits=10, right_digits=2, positive=True
    )
    source_link = factory.Faker("url")
    chart_link = factory.Faker("url")
    extra_link = factory.Faker("url")
