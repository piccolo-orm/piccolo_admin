"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
import os
import typing as t

from piccolo.table import Table
from piccolo.extensions.user.tables import BaseUser
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.session_auth.endpoints import session_login, session_logout
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Router, Route, BaseRoute, Mount
from starlette.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.exceptions import ExceptionMiddleware


ASSET_PATH = os.path.join(os.path.dirname(__file__), "dist")


class AdminRouter(Router):
    """
    The root returns a single page app. The other URLs are REST endpoints.
    """

    table: t.List[Table] = []
    auth_table: t.Type[BaseUser] = None
    template: str = ""

    def __init__(
        self, *tables: t.Type[Table], auth_table: t.Type[BaseUser] = BaseUser
    ) -> None:
        self.auth_table = auth_table

        with open(os.path.join(ASSET_PATH, "index.html")) as f:
            self.template = f.read()

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
            Route(
                path="/tables/",
                endpoint=self.get_table_list,
                methods=["GET", "POST", "DELETE"],
            ),
            Route(path="/login/", endpoint=session_login(), methods=["POST"]),
            Route(
                path="/logout/", endpoint=session_logout(), methods=["POST"]
            ),
        ]

        for table in tables:
            routes.append(
                Mount(
                    path=f"/tables/{table._meta.tablename}/",
                    app=PiccoloCRUD(table, read_only=False),
                )
            )

        self.tables = tables
        super().__init__(routes)

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    def get_table_list(self, request: Request) -> JSONResponse:
        return JSONResponse([i._meta.tablename for i in self.tables])


def create_admin(tables: t.Sequence[Table], auth_table: BaseUser):
    return ExceptionMiddleware(
        CORSMiddleware(
            AdminRouter(*tables, auth_table=auth_table),
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )
