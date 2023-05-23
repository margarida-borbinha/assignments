"""File Strategies for loading, cleaning and saving"""
import pathlib
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from life_expectancy.country import Country

FILE_DIR = pathlib.Path(__file__).parent.resolve()


class FileStrategy(ABC):
    """Abstract File Strategy"""

    def __validate_region(self, region: Country):
        if region.value not in Country.actual_countries():
            raise ValueError(f"Region {region.value} is not valid.")

    @abstractmethod
    def load_data(self, file: str) -> pd.DataFrame:
        """Loads the dataframe containing the raw
            European life expectancy data

        Returns:
            pd.DataFrame: Raw life expectancy dataframe
        """

    def clean_data(self, data: pd.DataFrame, region: Country) -> pd.DataFrame:
        """Cleans the dataset performing the following 5 steps:
        1. Transform the columns with the yearly information into two
            columns, one called year and another called value that
            contains the life expectancy in that year. This operation
            transforms the dataframe from a wide to a long format;
        2. Cleans the value column remove all the lowercase letters
            and casts the column value to be a numeric type, returning
            NaN when this convertion is not possible. The NaN values
            in this column are dropped;
        3. Cast "year" and "value" columns;
        4. Filter the data by the provided region.

        Args:
            data (pd.DataFrame): The dataframe to be cleaned
            region (Optional[str], optional): Region to filter the dataset on.
                Defaults to "PT".

        Returns:
            pd.DataFrame: The life expectancy dataset cleaned and
                filtered by the provided region
        """
        self.__validate_region(region)
        # 1st step
        data = data.melt(
            id_vars=["unit", "sex", "age", "region"], var_name="year"
        )

        # 2nd step
        data["value"] = data["value"].str.replace(r"[a-z]", "", regex=True)
        data["value"] = pd.to_numeric(data["value"], errors="coerce")
        data = data.dropna(subset=["value"])

        # 3rd step
        data["year"] = data["year"].astype(int)
        data["value"] = data["value"].astype(float)

        # 4th step
        data = data[data["region"] == region.value]

        return data

    @abstractmethod
    def save_data(self, data: pd.DataFrame, region: Country) -> None:
        """Saves the given data in the appropriate folder with the
            name following the name convention {region}_life_expectancy.csv

        Args:
            data (pd.DataFrame): The dataframe to be saved
            region (Optional[str], optional): The region used for filtering the
                data is the prefix of the file name. Defaults to "PT".
        """

    def main(
        self, file: str, region: Optional[Country] = Country.PT
    ) -> pd.DataFrame:
        """The main function that loads, cleans and saves in one go."""
        data = self.load_data(file)
        data = self.clean_data(data, region)
        self.save_data(data, region)
        return data


class TSVStrategy(FileStrategy):
    """Strategy for .tsv files"""

    def load_data(self, file: str) -> pd.DataFrame:
        data = pd.read_csv(f"{FILE_DIR}/data/{file}", sep="\t")

        return data

    def clean_data(
        self, data: pd.DataFrame, region: Optional[Country] = Country.PT
    ) -> pd.DataFrame:
        """Cleans the dataset performing the following 5 steps:
        1. Split the first column in the dataframe into "unit",
            "sex", "age", "region", because this values are separated
            using a comma and drop this column;
        2. Follow the cleaning steps common to all file strategies

        Returns:
            pd.DataFrame: The life expectancy dataset with unit, sex, age
                and region as columns
        """
        # 1st step
        data[["unit", "sex", "age", "region"]] = data[
            "unit,sex,age,geo\\time"
        ].str.split(",", expand=True)
        data = data.drop(columns=["unit,sex,age,geo\\time"])

        data = super().clean_data(data, region)
        return data

    def save_data(
        self, data: pd.DataFrame, region: Optional[Country] = Country.PT
    ) -> None:
        data.to_csv(
            f"{FILE_DIR}/data/{region.value.lower()}_life_expectancy.csv"
        )


class JSONStrategy(FileStrategy):
    """Strategy for .json files"""

    def load_data(self, file: str) -> pd.DataFrame:
        data = pd.read_json(f"{FILE_DIR}/data/{file}")

        return data

    def clean_data(
        self, data: pd.DataFrame, region: Optional[Country] = Country.PT
    ) -> pd.DataFrame:
        """Cleans the dataset performing the following 5 steps:
        1. Rename country column to region
        2. Follow the cleaning steps common to all file strategies

        Returns:
            pd.DataFrame: The life expectancy dataset with region as column
        """
        data = data.rename(columns={"country": "region"})
        return super().clean_data(data, region)

    def save_data(
        self, data: pd.DataFrame, region: Optional[Country] = Country.PT
    ) -> None:
        data.to_json(
            f"{FILE_DIR}/data/{region.value.lower()}_life_expectancy.json"
        )
