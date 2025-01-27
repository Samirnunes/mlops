# Prefect API and UI Server Deploy Guide

This repository contains a `Dockerfile` and an environment with `Poetry` that can be used to deploy a self-hosted Prefect server, considering your env vars are configured in AWS Systems Manager. Besides, the server has basic auth, that is, you must authenticate using an username and a password.

To effectively make the deploy, run the `Dockerfile` in an infrastructure in AWS ECS or similar. It is advisable to integrate the `Dockerfile` run in a CI/CD pipeline with build and deploy stages.

The necessary env vars are:

- `AWS_ACCESS_KEY_ID`
- `AWS_REGION`
- `AWS_SECRET_ACCESS_KEY`
- `PREFECT_API_DATABASE_CONNECTION_URL`
- `PREFECT_API_URL`
- `PREFECT_RUNNER_HEARTBEAT_FREQUENCY`
- `PREFECT_RUNNER_ENABLE`
- `PREFECT_RUNNER_MISSED_POOLS_TOLERANCE`
- `PREFECT_RUNNER_PROCESS_LIMIT`
- `PREFECT_RUNNER_POOL_FREQUENCY`
- `PREFECT_SERVER_API_HOST = 0.0.0.0`
- `PREFECT_SERVER_API_PORT = 80`
- `PREFECT_SERVER_API_AUTH_STRING` (must be in the format `<username>:<password>`)

Each description of the `PREFECT_` variables is present in the references:  

- https://docs-2.prefect.io/latest/api-ref/prefect/settings/
- https://docs-2.prefect.io/latest/guides/settings/

To authenticate in the API, you must configure in the client an env var called `PREFECT_API_AUTH_STRING` that must have the same value as the `PREFECT_SERVER_API_AUTH_STRING` server variable, and the env var `PREFECT_API_URL` with the same value as the server's.
