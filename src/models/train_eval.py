import os
import json
import click
import pandas as pd
import joblib as jb
import lightgbm as lgb
import mlflow
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.metrics import mean_absolute_error, mean_squared_error
from dotenv import load_dotenv


FEATURES = ['price', 'geo_lat', 'geo_lon', 'building_type', 'level', 'levels',
            'area', 'kitchen_area', 'object_type', 'year', 'month',
            'level_to_levels', 'area_to_rooms', 'cafes_0.012', 'cafes_0.08']


load_dotenv()
remote_server_uri = os.getenv("MLFLOW_TRACKING_URI")
experiment_name = "light_gbm"
mlflow.set_tracking_uri(remote_server_uri)
experiment_id = mlflow.set_experiment(experiment_name)


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path(),nargs=2 )
def train(input_paths: list[str], output_path: list[str]) -> None:
    """
    Train, eval the model and log params, metrics artifacts in MLflow 

    Args:
        input_paths (list[str]): train[0] and test[1] paths to dataframes
        output_path (list[str]): model[0] and score[1] artifact's paths
    """
    with mlflow.start_run(description="One of the describtion of the run", tags={"model": "lgbm", "case": "real_state"}):
        mlflow.get_artifact_uri()
        
        print(mlflow.get_artifact_uri())
        
        train_df = pd.read_csv(input_paths[0])
        test_df = pd.read_csv(input_paths[1])

        x_train = train_df.drop('price', axis=1)
        y_train = train_df['price']
        x_holdout = test_df.drop('price', axis=1)
        y_holdout = test_df['price']
        lgb_train = lgb.Dataset(x_train, y_train)
        lgb_eval = lgb.Dataset(x_holdout, y_holdout, reference=lgb_train)
        params = {
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': {'l1'},
            'max_depth': 11,
            'num_leaves': 120,
            'learning_rate': 0.25,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.9,
            'n_estimators': 1000,
            'bagging_freq': 2,
            'verbose': -1
        }

        # mlflow log lgbm params
        mlflow.log_params(params)

        gbm = lgb.train(params,
                        lgb_train,
                        num_boost_round=200,
                        valid_sets=lgb_eval,
                        verbose_eval=False,
                        early_stopping_rounds=30)  # categorical_feature=['building_type']
        jb.dump(gbm, output_path[0])

        y_predicted = gbm.predict(x_holdout, num_iteration=gbm.best_iteration)
        score = dict(
            mae=mean_absolute_error(y_holdout, y_predicted),
            rmse=mean_squared_error(y_holdout, y_predicted)
            )
        
        with open(output_path[1], "w") as score_file:
            json.dump(score, score_file, indent=4)
        
        # signature store metadata for input-output of the model in mlflow
        signature = infer_signature(x_holdout, y_predicted)

        # mlflow log lgbm metric score
        mlflow.log_metrics(score)
        mlflow.log_artifact(output_path[0])
        mlflow.lightgbm.log_model(lgb_model=gbm,
                                  artifact_path="lgbm_model",
                                  registered_model_name="real_estate_lgbm",
                                  signature=signature)


if __name__ == "__main__":
    train() # pylint: disable=no-value-for-parameter
