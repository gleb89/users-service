from logging import debug

from fastapi import Request
from starlette.middleware import Middleware
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send


class HTTPLogMiddleware():
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> ASGIApp:
        if scope["type"] == "http":
            request = Request(
                scope=scope,
                receive=receive)
            headers = Headers(
                scope=scope)

            debug(f"{request.method} {request.url}")

            debug("Params:")
            for name, value in request.path_params.items():
                debug(f"\t{name}: {value}")

            debug("Headers:")
            for name, value in headers.items():
                debug(f"\t{name}: {value}")

        return await self.app(
            scope=scope,
            receive=receive,
            send=send)


middleware = [
    Middleware(HTTPLogMiddleware),
]