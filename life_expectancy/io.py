"""
I/O module
"""

import pathlib
from typing import Optional

import pandas as pd

FILE_DIR = pathlib.Path(__file__).parent.resolve()


def load_data(
    file: Optional[str] = "eu_life_expectancy_raw.tsv",
) -> pd.DataFrame:
    """Loads the dataframe containing the raw
        European life expectancy data

    Returns:
        pd.DataFrame: Raw life expectancy dataframe
    """

    data = pd.read_csv(f"{FILE_DIR}/data/{file}", sep="\t")

    return data


def save_data(data: pd.DataFrame, region: Optional[str] = "PT") -> None:
    """Saves the given data in the appropriate folder with the
        name following the name convention {region}_life_expectancy.csv

    Args:
        data (pd.DataFrame): The dataframe to be saved
        region (Optional[str], optional): The region used for filtering the
            data is the prefix of the file name. Defaults to "PT".
    """

    data.to_csv(f"{FILE_DIR}/data/{region.lower()}_life_expectancy.csv")
