import click
import pandas as pd


FEATURES = ['price', 'geo_lat', 'geo_lon', 'building_type', 'level', 'levels',
            'area', 'kitchen_area', 'object_type', 'year', 'month',
            'level_to_levels', 'area_to_rooms', 'cafes_0.012', 'cafes_0.08']
DROP_DUPLICATES = ['geo_lat','geo_lon', 'level', 'area']
TRAIN_FRAQ = 0.75
SEED = 42


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path(exists=True), nargs=2)
def prepare_datasets(input_filepath: str, output_filepaths: list[str]) -> None:
    """_summary_

    Args:
        input_filepath (str): _description_
        output_filepaths (list[str]): _description_
    """
    df = pd.read_csv(input_filepath)
    df = df[FEATURES]
    df = df.drop_duplicates(subset=DROP_DUPLICATES, keep="last")
    
    train = df.sample(frac=TRAIN_FRAQ, random_state=SEED)
    test = df.drop(train.index, axis="index")
    
    train.to_csv(output_filepaths[0], index=False)
    test.to_csv(output_filepaths[1], index=False)
    
    
if __name__ == "__main__":
    prepare_datasets() # pylint: disable=no-value-for-parameter
