# 1.MLflow commands
- To run model locally: mlflow models serve --no-conda -m MODELPATH_FROM_MLFLOW -h 0.0.0.0 -p 5001
- To run model in docker: mlflow models build-docker -m MODELPATH_FROM_MLFLOW -n "real_state_lgbm"

In windows it is required create `credentials` file in C:\\Users\\your_user\\.aws in style:
```
[default]
aws_access_key_id=minioadmin
aws_secret_access_key=minioadmn
aws_buvket_name=mlops-course

[admin]
aws_access_key_id=minioadmin
aws_secret_access_key=minioadmin
```

# 2. Docker commands
- Build FastAPI service: `docker build -f Docker/model_service/Dockerfile -t model_service .`
- Build and run the whole app: `docker-compose up -d --build`

# 3. FastAPI test
Use `http://127.0.0.1:8003/invocations` and file `postman_sample_request` to fast-test the FastAPI service

# X. Course info

[Course ODS page](https://ods.ai/tracks/ml-in-production-spring-22)

[Sources and links](https://yandex.ru/q/article/osnovnaia_informatsiia_dlia_uchastnikov_418642d4/?utm_medium=share&utm_campaign=article)