# pylint: disable=missing-module-docstring
from click.testing import CliRunner
from src import select_region


# initialize runner
runner = CliRunner()


def test_cli_command():
    """check wether cli is working or not"""
    result = runner.invoke(select_region, 'data/raw/all_v2.csv data/interim/data_regional.csv 2661')
    assert result.exit_code == 0
