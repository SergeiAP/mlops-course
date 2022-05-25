# pylint: disable=missing-module-docstring
from click.testing import CliRunner
from src.data.get_osm_cafes_data import get_osm_cafes_data

# initialize runner
runner = CliRunner()


def test_cli_command():
    """check wether cli is working or not"""
    result = runner.invoke(
        get_osm_cafes_data,
        [
            "https://maps.mail.ru/osm/tools/overpass/api/interpreter?data=[out:json];nwr['addr:street'='Лиговский проспект']['addr:housenumber'=101];node[amenity=cafe](around:25000);out geom;",
            "data/external/data_cafes.geojson"
        ],
    )
    assert result.exit_code == 0
