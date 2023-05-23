"""Strategy Factory"""
import os
import pathlib
from typing import Union

import pandas as pd

from life_expectancy.file_strategies import JSONStrategy, TSVStrategy

FILE_DIR = pathlib.Path(__file__).parent.resolve()


class FileStrategyFactory:
    """
    A factory for creating the Strategies
    """

    def __init__(
        self,
        filepath_or_dataframe: Union[str, pd.DataFrame],
    ):
        self.file = None
        self.data = None
        if isinstance(filepath_or_dataframe, str):
            self.file = filepath_or_dataframe
        elif isinstance(filepath_or_dataframe, pd.DataFrame):
            self.data = filepath_or_dataframe

    def __is_tsv(self):
        return (
            self.file is not None and os.path.splitext(self.file)[1] == ".tsv"
        ) or (
            (self.data is not None)
            and "unit,sex,age,geo\\time" in self.data.columns
        )

    def __is_json(self):
        return (
            self.file is not None and os.path.splitext(self.file)[1] == ".json"
        ) or (
            self.data is not None
            and {
                "age",
                "country",
                "sex",
                "unit",
            }.issubset(set(self.data.columns))
        )

    def create_strategy(self):
        """Creates appropriated strategy for file type

        Raises:
            NotImplementedError: raises this exception if the file
                has no strategy

        Returns:
            FileStrategy: A strategy appropriated for the file
        """
        if self.__is_json():
            return JSONStrategy()
        if self.__is_tsv():
            return TSVStrategy()
        raise NotImplementedError(
            "There is no load data strategy for this file type."
        )
