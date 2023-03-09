"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `main` function and compare
    the output to the expected output"""
    main()
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_clean_data_argparse():
    """Run the `main` function and compare the output
    has results where the region is AL"""
    main("AL")
    al_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "al_life_expectancy.csv"
    )

    assert (al_life_expectancy_actual['region'] == 'AL').all()
