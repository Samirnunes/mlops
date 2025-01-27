import os

from pydantic import SecretStr

from prefect.server.api.server import create_app
from prefect.settings import Settings
from prefect.settings.models.api import APISettings
from prefect.settings.models.runner import RunnerServerSettings, RunnerSettings
from prefect.settings.models.server.api import ServerAPISettings
from prefect.settings.models.server.database import ServerDatabaseSettings
from prefect.settings.models.server.root import ServerSettings
from prefect.settings.models.worker import WorkerSettings, WorkerWebserverSettings
from prefect_server.api.config.auth import add_auth_middleware
from prefect_server.api.routes import health, metrics

settings = Settings(
    api=APISettings(url=os.environ["PREFECT_API_URL"]),
    runner=RunnerSettings(
        process_limit=int(os.environ["PREFECT_RUNNER_PROCESS_LIMIT"]),
        pool_frequency=int(os.environ["PREFECT_RUNNER_POOL_FREQUENCY"]),
        heartbeat_frequency=int(os.environ["PREFECT_RUNNER_HEARTBEAT_FREQUENCY"]),
        server=RunnerServerSettings(
            enable=bool(os.environ["PREFECT_RUNNER_ENABLE"]),
            host=os.environ["PREFECT_SERVER_API_HOST"],
            port=int(os.environ["PREFECT_SERVER_API_PORT"]),
            missed_polls_tolerance=int(
                os.environ["PREFECT_RUNNER_MISSED_POOLS_TOLERANCE"]
            ),
        ),
    ),
    server=ServerSettings(
        api=ServerAPISettings(
            host=os.environ["PREFECT_SERVER_API_HOST"],
            port=int(os.environ["PREFECT_SERVER_API_PORT"]),
        ),
        database=ServerDatabaseSettings(
            connection_url=SecretStr(
                os.environ["PREFECT_API_DATABASE_CONNECTION_URL"]
            )
        ),
    ),
    worker=WorkerSettings(
        webserver=WorkerWebserverSettings(
            host=os.environ["PREFECT_SERVER_API_HOST"],
            port=int(os.environ["PREFECT_SERVER_API_PORT"]),
        ),
    ),
)

app = create_app(settings)
app = add_auth_middleware(app)
app.include_router(health.router)
app.include_router(metrics.router)
