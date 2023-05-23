from life_expectancy.country import Country


def test_valid_countries():
    assert "EU28" not in Country.actual_countries()
