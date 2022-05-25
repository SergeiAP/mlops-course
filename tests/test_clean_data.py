# pylint: disable=missing-module-docstring
import great_expectations as ge
import pandas as pd
from click.testing import CliRunner
from src import clean_data

# initialize runner, which gives opportunities to check cli commands
runner = CliRunner()


def test_cli_commmand():
    """check wether cli is working or not"""
    result = runner.invoke(
        clean_data, "data/interim/data_regional.csv data/interim/data_cleaned.csv"
    )
    assert result.exit_code == 0


def test_output():
    """_summary_"""
    df = pd.read_csv("data/interim/data_cleaned.csv")
    df_ge = ge.from_pandas(df)

    expected_columns = [
        "price",
        "date",
        "geo_lat",
        "geo_lon",
        "building_type",
        "level",
        "levels",
        "rooms",
        "area",
        "kitchen_area",
        "object_type",
    ]
    assert (
        df_ge.expect_table_columns_to_match_ordered_list(
            column_list=expected_columns
        ).success
        is True
    )
    # assert df_ge.expect_column_values_to_be_unique(column="id").success is True is True
    assert (
        df_ge.expect_column_values_to_not_be_null(column="geo_lat").success
        is True
    )
    assert (
        df_ge.expect_column_values_to_be_of_type(
            column="kitchen_area", type_="float64"
        ).success
        is True
    )
    assert (
        df_ge.expect_column_values_to_match_strftime_format(
            column="date", strftime_format="%Y-%m-%d"
        ).success
        is True
    )
