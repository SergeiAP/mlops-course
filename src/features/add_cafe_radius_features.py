import click # pylint disable=missing-module-docstring
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


RADIUS_LIST = [0.002, 0.005, 0.08, 0.012]


def add_cafes_in_radius(gdf: gpd.GeoDataFrame, cafes_gdf: gpd.GeoDataFrame, radius: float) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        gdf (gpf.GeoDataFrame): _description_
        cafes_gdf (gpf.GeoDataFrame): _description_
        radius (float): _description_

    Returns:
        gpf.GeoDataFrame: _description_
    """
    gdf['cafes_' + str(radius)] = 0
    list_arrays = [ np.array((geom.xy[0][0], geom.xy[1][0])) for geom in cafes_gdf["geometry"] ]
    list_tuples = [tuple(x) for x in list_arrays]
    points_array = np.array(list_tuples)
    max_distance = radius
    for idx, geometry in gdf['geometry'].iteritems():
        current_flat_position = np.array([geometry.x, geometry.y])
        distance_array = np.sqrt(np.sum((points_array - current_flat_position) ** 2, 1))
        near_points = points_array[distance_array < max_distance]
        cafe_number = len(near_points)
        gdf['cafes_' + str(radius)].at[idx] = cafe_number
    return gdf



@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("input_cafepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def add_cafe_radius_features(input_filepath: str, input_cafepath: str, output_filepath: str) -> None:
    df = pd.read_csv(input_filepath)
    df['geometry'] = [Point(xy) for xy in zip(df.geo_lon, df.geo_lat)]
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    cafes_gdf = gpd.read_file(input_cafepath)
    cafes_gdf = cafes_gdf.set_geometry('geometry')

    for radius in RADIUS_LIST:
        print(f"Adding radius = {radius}")
        gdf = add_cafes_in_radius(gdf, cafes_gdf, radius)

    gdf.to_csv(output_filepath, index=False)

    
    
if __name__ == "__main__":
    add_cafe_radius_features() # pylint: disable=no-value-for-parameter
