import click
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.argument("region", type=click.INT)
def select_region(input_path: str, output_path: str, region: int) -> None:
    """Function selects the listings belonging to a specified region
        python -m src.data.select_region sata/raw/all_v2.csv \
        data/interim/data_regional.csv 2661
    Args:
        input_path (str): Path to read original DataFrame with all listings
        output_path (str): Path to save filtered DataFrame
        region (int): Selected region id
    """
    df = pd.read_csv(input_path)
    
    df = df[df['region'] == region]
    df.drop('region', axis=1, inplace=True)
    print(f'Selected {len(df)} samples in region {region}.')
    
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    select_region() # pylint: disable=no-value-for-parameter
