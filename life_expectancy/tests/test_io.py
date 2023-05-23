"""Tests for the I/O module"""
from unittest.mock import Mock, patch

import pandas as pd

from life_expectancy.country import Country
from life_expectancy.strategy_factory import FileStrategyFactory, TSVStrategy


def to_csv(file_path: str) -> None:
    print(f"Saving file {file_path}")


def test_load_tsv(life_expectancy):
    strategy = FileStrategyFactory(
        filepath_or_dataframe="eu_life_expectancy_raw.tsv"
    ).create_strategy()
    data = strategy.load_data(file="eu_life_expectancy_raw.tsv")
    pd.testing.assert_frame_equal(life_expectancy, data)


@patch("pandas.DataFrame.to_csv")
def test_save(to_csv_mock: Mock, sample_life_expectancy):
    to_csv_mock.side_effect = to_csv
    strategy = FileStrategyFactory(
        filepath_or_dataframe=sample_life_expectancy
    ).create_strategy()

    strategy.save_data(data=sample_life_expectancy, region=Country.PT)
    assert type(strategy) == TSVStrategy

    to_csv_mock.assert_called()
