"""
Cleaning module
"""

from typing import Optional
import argparse
import pathlib
import pandas as pd

FILE_DIR = pathlib.Path(__file__).parent.resolve()


def load_data() -> pd.DataFrame:
    """Loads the dataframe containing the raw
        European life expectancy data

    Returns:
        pd.DataFrame: Raw life expectancy dataframe
    """

    data = pd.read_csv(
        f"{FILE_DIR}/data/eu_life_expectancy_raw.tsv", sep="\t"
    )

    return data


def save_data(data: pd.DataFrame, region: Optional[str] = "PT") -> None:
    """Saves the given data in the appropriate folder with the
        name following the name convention {region}_life_expectancy.csv

    Args:
        data (pd.DataFrame): The dataframe to be saved
        region (Optional[str], optional): The region used for filtering the
            data is the prefix of the file name. Defaults to "PT".
    """

    data.to_csv(
        f"{FILE_DIR}/data/{region.lower()}_life_expectancy.csv",
        index=False
    )


def clean_data(data, region: Optional[str] = "PT") -> pd.DataFrame:
    """Cleans the dataset performing the following 5 steps:
        1. Split the first column in the dataframe into "unit",
            "sex", "age", "region", because this values are separated
            using a comma and drop this column;
        2. Transform the columns with the yearly information into two
            columns, one called year and another called value that
            contains the life expectancy in that year. This operation
            transforms the dataframe from a wide to a long format;
        3. Cleans the value column remove all the lowercase letters
            and casts the column value to be a numeric type, returning
            NaN when this convertion is not possible. The NaN values
            in this column are dropped;
        4. Cast "year" and "value" columns;
        5. Filter the data by the provided region.

    Args:
        data (pd.DataFrame): The dataframe to be cleaned
        region (Optional[str], optional): Region to filter the dataset on.
            Defaults to "PT".

    Returns:
        pd.DataFrame: The life expectancy dataset cleaned and filtered by the
            provided region
    """

    # 1st step
    data[["unit", "sex", "age", "region"]] = data[
        "unit,sex,age,geo\\time"
    ].str.split(",", expand=True)
    data = data.drop(columns=["unit,sex,age,geo\\time"])

    # 2nd step
    data = data.melt(id_vars=["unit", "sex", "age", "region"], var_name="year")

    # 3rd step
    data["value"] = data["value"].str.replace(r"[a-z]", "", regex=True)
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"])

    # 4th step
    data["year"] = data["year"].astype(int)
    data["value"] = data["value"].astype(float)

    # 5th step
    data = data[data["region"] == region]

    return data


def main(region: Optional[str] = "PT"):
    """The main function that loads, cleans and saves in one go.

    Args:
        region (Optional[str], optional): Region to filter the dataset on.
            Defaults to "PT".
    """
    data = load_data()
    data = clean_data(data, region)
    save_data(data, region)


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--region",
        default="PT",
        type=str,
        help="Region to filter the life expectancy data on on (default: PT)",
    )

    args = parser.parse_args()

    main(args.region)
