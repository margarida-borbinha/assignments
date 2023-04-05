from unittest.mock import Mock, patch

import pandas as pd

from life_expectancy.io import load_data, save_data


def to_csv(*args, **kwargs) -> None:
    print("Saving file")


def test_load(life_expectancy):
    data = load_data()
    pd.testing.assert_frame_equal(life_expectancy, data)


@patch("pandas.DataFrame.to_csv")
def test_save(to_csv_mock: Mock, sample_life_expectancy):
    to_csv_mock.side_effect = to_csv
    save_data(sample_life_expectancy, "test")

    to_csv_mock.assert_called()
