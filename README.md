### MLOps course Repository
==============================

[Course ODS page](https://ods.ai/tracks/ml-in-production-spring-22)

[Sources and links](https://yandex.ru/q/article/osnovnaia_informatsiia_dlia_uchastnikov_418642d4/?utm_medium=share&utm_campaign=article)

[MLflow commands]
- To run model locally: mlflow models serve --no-conda -m MODELPATH_FROM_MLFLOW -h 0.0.0.0 -p 8001
- To run model in docker: mlflow models build-docker -m MODELPATH_FROM_MLFLOW -n "real_state_lgbm"
