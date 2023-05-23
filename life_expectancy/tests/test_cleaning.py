"""Tests for the cleaning module"""
import pandas as pd
import pytest

from life_expectancy.country import Country
from life_expectancy.strategy_factory import FileStrategyFactory


def test_clean_data(sample_life_expectancy, pt_life_expectancy_expected):
    """Run the `main` function and compare
    the output to the expected output"""

    strategy = FileStrategyFactory(
        filepath_or_dataframe=sample_life_expectancy
    ).create_strategy()

    pt_life_expectancy_actual = strategy.clean_data(
        sample_life_expectancy, Country.PT
    )
    pt_life_expectancy_actual = pt_life_expectancy_actual.reset_index(
        drop=True
    )

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual,
        pt_life_expectancy_expected,
    )


def test_clean_data_argparse():
    """Run the `main` function and compare the output
    has results where the region is AL"""

    strategy = FileStrategyFactory(
        filepath_or_dataframe="eu_life_expectancy_raw.tsv"
    ).create_strategy()
    al_life_expectancy_actual = strategy.main(
        "eu_life_expectancy_raw.tsv",  region=Country.AL
    )

    assert (al_life_expectancy_actual["region"] == "AL").all()


def test_clean_data_json():
    """Run the `main` function and compare the output
    has results where the region is AL"""

    strategy = FileStrategyFactory(
        filepath_or_dataframe="eurostat_life_expect.json",
    ).create_strategy()
    al_life_expectancy_actual = strategy.main(
        "eurostat_life_expect.json", region=Country.AL
    )

    assert (al_life_expectancy_actual["region"] == "AL").all()


def test_invalid_region():
    """Run the `main` function with an invalid region"""
    with pytest.raises(ValueError):
        strategy = FileStrategyFactory(
            filepath_or_dataframe="eu_life_expectancy_raw.tsv",
        ).create_strategy()

        strategy.main(
            "eu_life_expectancy_raw.tsv",
            region=Country.EEA30_2007,
        )


def test_invalid_format():
    """Run the `main` function with an invalid file format"""
    with pytest.raises(NotImplementedError):
        _ = FileStrategyFactory(
            filepath_or_dataframe="test.txt"
        ).create_strategy()
