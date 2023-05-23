"""
Cleaning module
"""

import argparse

from life_expectancy.strategy_factory import FileStrategyFactory

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

    strategy = FileStrategyFactory(
        "eu_life_expectancy_raw.tsv"
    ).create_strategy()

    strategy.main("eu_life_expectancy_raw.tsv", args.region)
