"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
import os
import typing as t

from piccolo.table import Table
from piccolo.extensions.user import BaseUser
from piccolo_api.endpoints.crud import PiccoloCRUD
# from piccolo_api.endpoints.auth import JWTLogin
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Router, Route, BaseRoute, Mount
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.exceptions import ExceptionMiddleware


ASSET_PATH = os.path.join(
    os.path.dirname(__file__),
    'dist'
)


class AdminRouter(Router):
    """
    The root returns a single page app. The other URLs are REST endpoints.
    """
    table: t.List[Table] = []
    auth_table: BaseUser = None
    template: str = ''

    def __init__(self, *tables: Table, auth_table: BaseUser) -> None:
        self.auth_table = auth_table

        with open(os.path.join(ASSET_PATH, 'index.html')) as f:
            self.template = f.read()

        routes: t.List[BaseRoute] = [
            Route(
                path='/',
                endpoint=self.get_root,
                methods=['GET']
            ),
            Mount(
                path='/css',
                app=StaticFiles(
                    directory=os.path.join(ASSET_PATH, 'css')
                ),
            ),
            Mount(
                path='/js',
                app=StaticFiles(
                    directory=os.path.join(ASSET_PATH, 'js')
                ),
            ),
            Route(
                path='/tables/',
                endpoint=self.get_table_list,
                methods=['GET', 'POST', 'DELETE']
            ),
            Route(
                path='/login/',
                endpoint=self.login,
                methods=['GET', 'POST']
            )
        ]

        for table in tables:
            routes.append(Mount(
                path=f'/tables/{table.__name__.lower()}/',
                app=PiccoloCRUD(table, read_only=False)
            ))

        self.tables = tables
        super().__init__(routes)

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    async def login(self, request: Request) -> Response:
        """
        One issue is ... not everyone should be able to login to the admin.

        Need an admin field as part of the User, or a more generic
        permissions system, which accepts any arbitrary list of strings ...
        """
        # TODO - use JWT login endpoint instead
        if request.method == 'GET':
            # request.headers['cookie']
            return HTMLResponse(
                content='<p>Login</p>',
                headers={'Set-Cookie': 'foo=bar; HttpOnly'}
            )
        elif request.method == 'POST':
            # TODO - only if they are admins ...
            user_id = await self.auth_table.login('dan', '123')
            # If login is successful, we need their token.
            print(user_id)
            return JSONResponse({
                'user_id': 123,
                'token': 'abc123'
            })
        else:
            return HTMLResponse()

    def get_table_list(self, request: Request) -> JSONResponse:
        return JSONResponse([
            i.__name__.lower() for i in self.tables
        ])


def create_admin(tables: t.Sequence[Table], auth_table: BaseUser):
    return ExceptionMiddleware(
        CORSMiddleware(
            AdminRouter(*tables, auth_table=auth_table),
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*']
        )
    )
