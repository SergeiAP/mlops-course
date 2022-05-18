import pandas as pd # pylint: disable=missing-module-docstring
import click
import geopandas as gpd
import requests
from shapely.geometry import Point


@click.command()
@click.argument("query_string", type=click.STRING)
@click.argument("output_path", type=click.Path())
def get_osm_cafes_data(query_string: str, output_path: str) -> None:
    """Make geodataframe from Overpass API

    Args:
        query_string (str): Ovepass API query string
        output_path (str): Path to save cafe data
    """
    # Retrieve URL contents, verify=False to disable SSL
    resp = requests.get(query_string, verify=False)

    # Make dataframe
    df = pd.DataFrame(resp.json()['elements'])

    # Convert to geodataframe
    df['geometry'] = [Point(xy) for xy in zip(df.lon, df.lat)]
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    gdf.to_file(output_path, driver='GeoJSON')


if __name__ == "__main__":
    get_osm_cafes_data() # pylint: disable=no-value-for-parameter
