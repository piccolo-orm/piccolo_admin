"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
from __future__ import annotations
from functools import partial
import os
import typing as t

from piccolo.table import Table
from piccolo.extensions.user.tables import BaseUser

from piccolo_admin import __VERSION__ as piccolo_admin_version
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.rate_limiting.middleware import (
    RateLimitingMiddleware,
    RateLimitProvider,
    InMemoryLimitProvider,
)
from piccolo_api.session_auth.endpoints import session_login, session_logout
from piccolo_api.session_auth.tables import SessionsBase
from piccolo_api.session_auth.middleware import SessionsAuthBackend

from starlette.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
from starlette.routing import Router, Route, BaseRoute, Mount
from starlette.staticfiles import StaticFiles
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware


ASSET_PATH = os.path.join(os.path.dirname(__file__), "dist")


def handle_auth_exception(request: Request, exc: Exception):
    return JSONResponse({"error": "Auth failed"}, status_code=401)


class AdminRouter(Router):
    """
    The root returns a single page app. The other URLs are REST endpoints.
    """

    table: t.List[Table] = []
    auth_table: t.Type[BaseUser] = BaseUser
    template: str = ""

    def __init__(
        self,
        *tables: t.Type[Table],
        auth_table: t.Type[BaseUser] = BaseUser,
        session_table: t.Type[SessionsBase] = SessionsBase,
        page_size: int = 15,
        read_only: bool = False,
        rate_limit_provider: t.Optional[RateLimitProvider] = None,
    ) -> None:
        self.auth_table = auth_table

        with open(os.path.join(ASSET_PATH, "index.html")) as f:
            self.template = f.read()

        auth_middleware = partial(
            AuthenticationMiddleware,
            backend=SessionsAuthBackend(
                auth_table=auth_table, session_table=session_table,
            ),
            on_error=handle_auth_exception,
        )

        if not rate_limit_provider:
            rate_limit_provider = InMemoryLimitProvider(
                limit=1000, timespan=300
            )

        table_routes: t.List[BaseRoute] = [
            Mount(
                path=f"/{table._meta.tablename}/",
                app=PiccoloCRUD(
                    table, read_only=read_only, page_size=page_size
                ),
            )
            for table in tables
        ]
        table_routes += [
            Route(path="/", endpoint=self.get_table_list, methods=["GET"],)
        ]

        routes: t.List[BaseRoute] = [
            Route(path="/", endpoint=self.get_root, methods=["GET"]),
            Mount(
                path="/css",
                app=StaticFiles(directory=os.path.join(ASSET_PATH, "css")),
            ),
            Mount(
                path="/js",
                app=StaticFiles(directory=os.path.join(ASSET_PATH, "js")),
            ),
            Mount(
                path="/api",
                app=Router(
                    [
                        Mount(
                            path="/tables/",
                            app=auth_middleware(Router(table_routes)),
                        ),
                        Route(
                            path="/login/",
                            endpoint=RateLimitingMiddleware(
                                app=session_login(
                                    auth_table=self.auth_table,
                                    session_table=session_table,
                                ),
                                provider=rate_limit_provider,
                            ),
                            methods=["POST"],
                        ),
                        Route(
                            path="/logout/",
                            endpoint=session_logout(
                                session_table=session_table
                            ),
                            methods=["POST"],
                        ),
                        Mount(
                            path="/user/",
                            app=auth_middleware(
                                Router(
                                    [Route(path="/", endpoint=self.get_user)]
                                )
                            ),
                        ),
                        Mount(
                            path="/meta/",
                            app=auth_middleware(
                                Router(
                                    [Route(path="/", endpoint=self.get_meta)]
                                )
                            ),
                        ),
                    ]
                ),
            ),
        ]

        self.tables = tables
        super().__init__(routes)

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    def get_user(self, request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "username": request.user.display_name,
                "user_id": request.user.user_id,
            }
        )

    ###########################################################################

    def get_meta(self, request: Request) -> JSONResponse:
        return JSONResponse({"piccolo_admin_version": piccolo_admin_version})

    ###########################################################################

    def get_table_list(self, request: Request) -> JSONResponse:
        return JSONResponse([i._meta.tablename for i in self.tables])


def get_all_tables(
    tables: t.Sequence[t.Type[Table]],
) -> t.Sequence[t.Type[Table]]:
    """
    Fetch any related tables, and include them.
    """
    output: t.List[t.Type[Table]] = []

    def get_references(table: t.Type[Table]):
        references = [
            i._foreign_key_meta.references
            for i in table._meta.foreign_key_columns
        ]
        for reference in references:
            if reference not in output:
                output.append(reference)
                get_references(reference)

    for table in tables:
        if table not in output:
            output.append(table)
        get_references(table)

    return output


def create_admin(
    tables: t.Sequence[t.Type[Table]],
    auth_table: t.Type[BaseUser] = BaseUser,
    session_table: t.Type[SessionsBase] = SessionsBase,
    page_size: int = 15,
    read_only: bool = False,
    auto_include_related=True,
):
    """
    :param page_size: The number of results shown on each page.
    :param read_only: Makes all non auth endpoints only respond to GET
    requests.
    :param auto_include_related: If a table has foreign keys to other tables,
    those tables will also be included in the admin by default, if not already
    specified. Otherwise the admin won't work as expected.
    """
    if auto_include_related:
        tables = get_all_tables(tables)

    return ExceptionMiddleware(
        CSRFMiddleware(
            AdminRouter(
                *tables,
                auth_table=auth_table,
                session_table=session_table,
                read_only=read_only,
            ),
        )
    )
