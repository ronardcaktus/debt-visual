from apps import utils


def test_format_country_or_continent_function():
    region1 = "south_america"
    region2 = "europe"
    contient1 = "south_america"
    contient2 = "australia"

    assert utils.format_country_or_continent(region1) == "South America"
    assert utils.format_country_or_continent(region2) == "Europe"
    assert utils.format_country_or_continent(contient1) == "South America"
    assert utils.format_country_or_continent(contient2) == "Australia"
