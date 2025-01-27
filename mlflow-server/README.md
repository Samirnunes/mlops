# MLflow Server Deploy Guide

This repository contains a `Dockerfile` and an environment with `Poetry` that can be used to deploy a self-hosted MLflow server, considering your env vars are configured in AWS Systems Manager. Besides, the server has basic auth, that is, you must authenticate using an username and a password.

The necessary env vars are:

- `AWS_ACCESS_KEY_ID`
- `AWS_DEFAULT_REGION`
- `AWS_SECRET_ACCESS_KEY`
- `MLFLOW_ARTIFACTS_DESTINATION`
- `MLFLOW_SERVE_ARTIFACTS`
- `MLFLOW_TRACKING_USERNAME`
- `MLFLOW_TRACKING_PASSWORD`
- `MLFLOW_BACKEND_STORE_URI`
- `MLFLOW_HOST = 0.0.0.0`
- `MLFLOW_PORT = 80`

Each description of the `MLFLOW_` variables is present in the reference:  https://mlflow.org/docs/latest/cli.html
