"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
from __future__ import annotations
from datetime import timedelta
from functools import partial
import os
import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIWrapper, FastAPIKwargs
from piccolo_api.rate_limiting.middleware import (
    RateLimitingMiddleware,
    RateLimitProvider,
    InMemoryLimitProvider,
)
from piccolo_api.session_auth.endpoints import session_login, session_logout
from piccolo_api.session_auth.tables import SessionsBase
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from pydantic import BaseModel

from fastapi import FastAPI
from starlette.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from .version import __VERSION__ as PICCOLO_ADMIN_VERSION

if t.TYPE_CHECKING:
    from piccolo.table import Table


ASSET_PATH = os.path.join(os.path.dirname(__file__), "dist")


class UserResponseModel(BaseModel):
    username: str
    user_id: str


class MetaResponseModel(BaseModel):
    piccolo_admin_version: str
    site_name: str


def handle_auth_exception(request: Request, exc: Exception):
    return JSONResponse({"error": "Auth failed"}, status_code=401)


class AdminRouter(FastAPI):
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
        session_expiry: timedelta = timedelta(hours=1),
        max_session_expiry: timedelta = timedelta(days=7),
        increase_expiry: t.Optional[timedelta] = timedelta(minutes=20),
        page_size: int = 15,
        read_only: bool = False,
        rate_limit_provider: t.Optional[RateLimitProvider] = None,
        production: bool = False,
        site_name: str = "Piccolo Admin",
    ) -> None:
        super().__init__(
            title=site_name, description="Piccolo API documentation"
        )

        self.auth_table = auth_table
        self.site_name = site_name
        self.tables = tables

        with open(os.path.join(ASSET_PATH, "index.html")) as f:
            self.template = f.read()

        #######################################################################

        api_app = FastAPI()

        for table in tables:
            FastAPIWrapper(
                root_url=f"/tables/{table._meta.tablename}/",
                fastapi_app=api_app,
                piccolo_crud=PiccoloCRUD(
                    table=table, read_only=read_only, page_size=page_size
                ),
                fastapi_kwargs=FastAPIKwargs(
                    all_routes={
                        "tags": [f"{table._meta.tablename.capitalize()}"]
                    },
                ),
            )

        api_app.add_api_route(
            path="/tables/",
            endpoint=self.get_table_list,
            methods=["GET"],
            response_model=t.List[str],
            tags=["Tables"],
        )

        api_app.add_api_route(
            path="/meta/",
            endpoint=self.get_meta,
            methods=["GET"],
            tags=["Meta"],
            response_model=MetaResponseModel,
        )

        api_app.add_api_route(
            path="/user/",
            endpoint=self.get_user,
            methods=["GET"],
            tags=["User"],
            response_model=UserResponseModel,
        )

        #######################################################################

        auth_app = FastAPI()

        if not rate_limit_provider:
            rate_limit_provider = InMemoryLimitProvider(
                limit=1000, timespan=300
            )

        auth_app.mount(
            path="/login/",
            app=RateLimitingMiddleware(
                app=session_login(
                    auth_table=self.auth_table,
                    session_table=session_table,
                    session_expiry=session_expiry,
                    max_session_expiry=max_session_expiry,
                    redirect_to=None,
                    production=production,
                ),
                provider=rate_limit_provider,
            ),
        )

        auth_app.add_route(
            path="/logout/",
            route=session_logout(session_table=session_table),
            methods=["POST"],
        )

        #######################################################################

        self.router.add_route(
            path="/", endpoint=self.get_root, methods=["GET"]
        )

        self.mount(
            path="/css",
            app=StaticFiles(directory=os.path.join(ASSET_PATH, "css")),
        )

        self.mount(
            path="/js",
            app=StaticFiles(directory=os.path.join(ASSET_PATH, "js")),
        )

        auth_middleware = partial(
            AuthenticationMiddleware,
            backend=SessionsAuthBackend(
                auth_table=auth_table,
                session_table=session_table,
                admin_only=True,
                increase_expiry=increase_expiry,
            ),
            on_error=handle_auth_exception,
        )

        self.mount(path="/api", app=auth_middleware(api_app))
        self.mount(path="/auth", app=auth_app)

        # We make the meta endpoint available without auth, because it contains
        # the site name.
        self.add_api_route("/meta/", endpoint=self.get_meta)

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    def get_user(self, request: Request) -> UserResponseModel:
        return UserResponseModel(
            username=request.user.display_name, user_id=request.user.user_id,
        )

    ###########################################################################

    def get_meta(self, request: Request) -> MetaResponseModel:
        return MetaResponseModel(
            piccolo_admin_version=PICCOLO_ADMIN_VERSION,
            site_name=self.site_name,
        )

    ###########################################################################

    def get_table_list(self, request: Request) -> t.List[str]:
        """
        Returns a list of all tables registered with the admin.
        """
        return [i._meta.tablename for i in self.tables]

    ###########################################################################

    def get_site_name(self, request: Request) -> JSONResponse:
        return JSONResponse({"site_name": self.site_name})


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
    session_expiry: timedelta = timedelta(hours=1),
    max_session_expiry: timedelta = timedelta(days=7),
    increase_expiry: t.Optional[timedelta] = timedelta(minutes=20),
    page_size: int = 15,
    read_only: bool = False,
    rate_limit_provider: t.Optional[RateLimitProvider] = None,
    production: bool = False,
    site_name: str = "Piccolo Admin",
    auto_include_related: bool = True,
    allowed_hosts: t.Sequence[str] = [],
):
    """
    :param tables:
        Each of the tables will be added to the admin.
    :param auth_table:
        Either a BaseUser, or BaseUser subclass table, which is used for
        fetching users.
    :param session_table:
        Either a SessionBase, or SessionBase subclass table, which is used
        for storing and querying session tokens.
    :param session_expiry:
        How long a session is valid for.
    :param max_session_expiry:
        The maximum time a session is valid for, taking into account any
        refreshes using `increase_expiry`.
    :param increase_expiry:
        If set, the `session_expiry` will be increased by this amount if it's
        close to expiry.
    :param page_size:
        The admin API paginates content - this sets the default number of
        results on each page.
    :param read_only:
        If True, all non auth endpoints only respond to GET requests - the
        admin can still be viewed, and the data can be filtered. Useful for
        creating online demos.
    :param rate_limit_provider:
        Rate limiting middleware is used to protect the login endpoint
        against brute force attack. If not set, an InMemoryLimitProvider
        will be configured with reasonable defaults.
    :param production:
        If True, the admin will enforce stronger security - for example,
        the cookies used will be secure, meaning they are only sent over
        HTTPS.
    :param site_name:
        Specify a different site name in the admin UI (default Piccolo Admin).
    :param auto_include_related:
        If a table has foreign keys to other tables, those tables will also be
        included in the admin by default, if not already specified. Otherwise
        the admin won't work as expected.
    :param allowed_hosts:
        This is used by the CSRF middleware as an additional layer of
        protection when the admin is run under HTTPS. It must be a sequence of
        strings, such as ['my_site.com'].
    """

    if auto_include_related:
        tables = get_all_tables(tables)

    return ExceptionMiddleware(
        CSRFMiddleware(
            AdminRouter(
                *tables,
                auth_table=auth_table,
                session_table=session_table,
                session_expiry=session_expiry,
                max_session_expiry=max_session_expiry,
                increase_expiry=increase_expiry,
                page_size=page_size,
                read_only=read_only,
                rate_limit_provider=rate_limit_provider,
                production=production,
                site_name=site_name,
            ),
            allowed_hosts=allowed_hosts,
        )
    )
