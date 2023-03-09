"""
Cleaning module
"""

import pandas as pd
import argparse
from typing import Optional


def clean_data(country: Optional[str] = "PT") -> None:
    """Reads the eu_life_expectancy_raw.tsv files and transforms it into a clean csv file
    having only the portuguese data.
    """
    data = pd.read_csv("./life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t")
    data[["unit", "sex", "age", "region"]] = data["unit,sex,age,geo\\time"].str.split(
        ",", expand=True
    )
    data = data.drop(columns=["unit,sex,age,geo\\time"])
    data = data.melt(id_vars=["unit", "sex", "age", "region"], var_name="year")

    data["value"] = data["value"].str.replace(r"[a-z]", "", regex=True)
    data["year"] = data["year"].astype(int)
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"])
    data["value"] = data["value"].astype(float)
    data = data[data["region"] == country]
    data.to_csv(
        f"./life_expectancy/data/{country.lower()}_life_expectancy.csv",
        index=False
    )

    return data


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser()

    parser.add_argument("country", type=str)
    parser.add_argument("-c", "--country", action="store_true")

    args = parser.parse_args()

    clean_data(args.country)
