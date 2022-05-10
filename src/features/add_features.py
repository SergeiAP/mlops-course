import click
import numpy as np
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def add_features(input_path: str, output_path: str) -> None:
    """_summary_

    Args:
        input_path (str): _description_
        output_path (str): _description_
    """
    df = pd.read_csv(input_path)
    
    # Replace "date" with numeric features for year and month.
    df["date"] = pd.to_datetime(df["date"])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df.drop('date', axis=1, inplace=True)
    # Apartment floor in relation to total number of floors.
    df['level_to_levels'] = df['level'] / df['levels']
    # Average size of room in the apartment.
    df['area_to_rooms'] = (df['area'] / df['rooms']).abs()
    # Fix division by zero.
    df.loc[df['area_to_rooms'] == np.inf, 'area_to_rooms'] = \
        df.loc[df['area_to_rooms'] == np.inf, 'area']
    
    df.to_csv(output_path, index=False)
    
    
if __name__ == "__main__":
    add_features() # pylint: disable=no-value-for-parameter
