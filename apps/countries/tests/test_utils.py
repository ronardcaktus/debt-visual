from apps import utils


def test_format_country_or_contient_function():
    region1 = "south_america"
    region2 = "europe"
    contient1 = "south_america"
    contient2 = "australia"

    assert utils.format_country_or_contient(region1) == "South America"
    assert utils.format_country_or_contient(region2) == "Europe"
    assert utils.format_country_or_contient(contient1) == "South America"
    assert utils.format_country_or_contient(contient2) == "Australia"
