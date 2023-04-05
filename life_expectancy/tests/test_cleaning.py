"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data, main


def test_clean_data(sample_life_expectancy, pt_life_expectancy_expected):
    """Run the `main` function and compare
    the output to the expected output"""
    pt_life_expectancy_actual = clean_data(sample_life_expectancy)
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
    al_life_expectancy_actual = main("eu_life_expectancy_raw.tsv", "AL")

    assert (al_life_expectancy_actual["region"] == "AL").all()
