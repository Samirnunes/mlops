import base64

from fastapi import FastAPI, Response
from pydantic_settings import BaseSettings
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse


class _AuthConfig(BaseSettings):
    PREFECT_SERVER_API_AUTH_STRING: str
    PREFECT_API_KEY: str


_config = _AuthConfig()
_user_auth = "Basic " + base64.b64encode(
    _config.PREFECT_SERVER_API_AUTH_STRING.encode("utf-8")
).decode("utf-8")


class CustomAuth(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> None | tuple[AuthCredentials, SimpleUser]:
        if conn.url.path == "/v1/health" or conn.url.path == "/v1/metrics":
            return None
        if "Authorization" not in conn.headers:
            raise AuthenticationError("no token")
        auth = conn.headers["Authorization"]
        if auth == _user_auth:
            return AuthCredentials(["auth"]), SimpleUser("user")
        raise AuthenticationError("invalid token")


def handler_error(conn: HTTPConnection, exc: Exception) -> Response:
    return PlainTextResponse(
        "Login required",
        401,
        headers={"WWW-Authenticate": f'Basic realm="Unauthorized: {exc}"'},
    )


def add_auth_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        AuthenticationMiddleware,
        backend=CustomAuth(),
        on_error=handler_error,
    )
    return app
