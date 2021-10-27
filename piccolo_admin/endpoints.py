"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
from __future__ import annotations

import inspect
import json
import os
import typing as t
from dataclasses import dataclass
from datetime import timedelta
from functools import partial

import pydantic
from fastapi import FastAPI
from piccolo.apps.user.tables import BaseUser
from piccolo.columns.reference import LazyTableReference
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper
from piccolo_api.openapi.endpoints import swagger_ui
from piccolo_api.rate_limiting.middleware import (
    InMemoryLimitProvider,
    RateLimitingMiddleware,
    RateLimitProvider,
)
from piccolo_api.session_auth.endpoints import session_login, session_logout
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from piccolo_api.session_auth.tables import SessionsBase
from pydantic import BaseModel, ValidationError
from starlette.exceptions import ExceptionMiddleware, HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from .version import __VERSION__ as PICCOLO_ADMIN_VERSION

if t.TYPE_CHECKING:  # pragma: no cover
    from piccolo.columns.base import Column
    from piccolo.table import Table


ASSET_PATH = os.path.join(os.path.dirname(__file__), "dist")


class UserResponseModel(BaseModel):
    username: str
    user_id: str


class MetaResponseModel(BaseModel):
    piccolo_admin_version: str
    site_name: str


@dataclass
class TableConfig:
    """
    Gives the user more control over how a ``Table`` appears in the UI.

    :param visible_columns:
        If specified, only these columns will be shown in the list view of the
        UI. This is useful when you have a lot of columns.
    :param exclude_visible_columns:
        You can specify this instead of ``visible_columns``, in which case all
        of the ``Table`` columns except the ones specified will be shown in the
        list view.
    :param visible_filters:
        If specified, only these columns will be shown in the filter sidebar
        of the UI. This is useful when you have a lot of columns.
    :param exclude_visible_filters:
        You can specify this instead of ``visible_filters``, in which case all
        of the ``Table`` columns except the ones specified will be shown in the
        filter sidebar.

    """

    table_class: t.Type[Table]
    visible_columns: t.Optional[t.List[Column]] = None
    exclude_visible_columns: t.Optional[t.List[Column]] = None
    visible_filters: t.Optional[t.List[Column]] = None
    exclude_visible_filters: t.Optional[t.List[Column]] = None

    def __post_init__(self):
        if self.visible_columns and self.exclude_visible_columns:
            raise ValueError(
                "Only specify ``visible_columns`` or "
                "``exclude_visible_columns``."
            )

        if self.visible_filters and self.exclude_visible_filters:
            raise ValueError(
                "Only specify ``visible_filters`` or "
                "``exclude_visible_filters``."
            )

    def _get_columns(
        self,
        include_columns: t.Optional[t.List[Column]],
        exclude_columns: t.Optional[t.List[Column]],
        all_columns: t.List[Column],
    ) -> t.List[Column]:
        if include_columns and not exclude_columns:
            return include_columns

        if exclude_columns and not include_columns:
            column_names = (i._meta.name for i in exclude_columns)
            return [i for i in all_columns if i._meta.name not in column_names]

        return all_columns

    def get_visible_columns(self) -> t.List[Column]:
        return self._get_columns(
            include_columns=self.visible_columns,
            exclude_columns=self.exclude_visible_columns,
            all_columns=self.table_class._meta.columns,
        )

    def get_visible_column_names(self) -> t.Tuple[str, ...]:
        return tuple(i._meta.name for i in self.get_visible_columns())

    def get_visible_filters(self) -> t.List[Column]:
        return self._get_columns(
            include_columns=self.visible_filters,
            exclude_columns=self.exclude_visible_filters,
            all_columns=self.table_class._meta.columns,
        )

    def get_visible_filter_names(self) -> t.Tuple[str, ...]:
        return tuple(i._meta.name for i in self.get_visible_filters())


@dataclass
class FormConfig:
    """
    Used to specify forms, which are passed into ``create_admin``.

    :param name:
        This will be displayed in the UI in the sidebar.
    :param pydantic_model:
        This determines which fields to display in the form, and is used to
        deserialise the responses.
    :param endpoint:
        Your custom handler, which accepts two arguments - the FastAPI /
        Starlette request object, in case you want to access the cookies /
        headers / logged in user (via `request.user`). And secondly an instance
        of the Pydantic model. If it returns a string, it will be shown to
        the user in the UI as the success message. For example ``'Successfully
        sent email'``. The endpoint can be a normal function or async function.
    :param description:
        An optional description which is shown in the UI to explain to the user
        what the form is for.

    Here's a full example:

    .. code-block:: python

        class MyModel(pydantic.BaseModel):
            message: str

        def my_endpoint(request: Request, data: MyModel):
            print(f"I received {data.message}")

            # If we're not happy with the data raise a ValueError
            # The message inside the exception will be displayed in the UI.
            raise ValueError("We were unable to process the form.")

            # If we're happy with the data, just return a string, which
            # will be displayed in the UI.
            return "Successful."

        config = FormConfig(
            name="My Form",
            pydantic_model=MyModel,
            endpoint=my_endpoint
        )

    """

    name: str
    pydantic_model: t.Type[BaseModel]
    endpoint: t.Callable[
        [Request, pydantic.BaseModel],
        t.Union[str, None, t.Coroutine],
    ]
    description: t.Optional[str] = None

    def __post_init__(self):
        self.slug = self.name.replace(" ", "-").lower()


class FormConfigResponseModel(BaseModel):
    name: str
    slug: str
    description: t.Optional[str] = None


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
        *tables: t.Union[t.Type[Table], TableConfig],
        forms: t.List[FormConfig] = [],
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

        #######################################################################
        # Convert any table arguments which are plain ``Table`` classes into
        # ``TableConfig`` instances.

        table_configs: t.List[TableConfig] = []

        for table in tables:
            if isinstance(table, TableConfig):
                table_configs.append(table)
            else:
                table_configs.append(TableConfig(table_class=table))

        self.table_configs = table_configs

        #######################################################################

        self.auth_table = auth_table
        self.site_name = site_name
        self.forms = forms
        self.form_config_map = {form.slug: form for form in self.forms}

        with open(os.path.join(ASSET_PATH, "index.html")) as f:
            self.template = f.read()

        #######################################################################

        api_app = FastAPI(docs_url=None)
        api_app.mount("/docs/", swagger_ui(schema_url="../openapi.json"))

        for table_config in table_configs:
            table_class = table_config.table_class
            visible_column_names = table_config.get_visible_column_names()
            visible_filter_names = table_config.get_visible_filter_names()
            FastAPIWrapper(
                root_url=f"/tables/{table_class._meta.tablename}/",
                fastapi_app=api_app,
                piccolo_crud=PiccoloCRUD(
                    table=table_class,
                    read_only=read_only,
                    page_size=page_size,
                    schema_extra={
                        "visible_column_names": visible_column_names,
                        "visible_filter_names": visible_filter_names,
                    },
                ),
                fastapi_kwargs=FastAPIKwargs(
                    all_routes={
                        "tags": [f"{table_class._meta.tablename.capitalize()}"]
                    },
                ),
            )

        api_app.add_api_route(
            path="/tables/",
            endpoint=self.get_table_list,  # type: ignore
            methods=["GET"],
            response_model=t.List[str],
            tags=["Tables"],
        )

        api_app.add_api_route(
            path="/meta/",
            endpoint=self.get_meta,  # type: ignore
            methods=["GET"],
            tags=["Meta"],
            response_model=MetaResponseModel,
        )

        api_app.add_api_route(
            path="/forms/",
            endpoint=self.get_forms,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
            response_model=t.List[FormConfigResponseModel],
        )

        api_app.add_api_route(
            path="/forms/{form_slug:str}/",
            endpoint=self.get_single_form,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
        )

        api_app.add_api_route(
            path="/forms/{form_slug:str}/schema/",
            endpoint=self.get_single_form_schema,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
        )

        api_app.add_api_route(
            path="/forms/{form_slug:str}/",
            endpoint=self.post_single_form,  # type: ignore
            methods=["POST"],
            tags=["Forms"],
        )

        api_app.add_api_route(
            path="/user/",
            endpoint=self.get_user,  # type: ignore
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
        self.add_api_route("/meta/", endpoint=self.get_meta)  # type: ignore

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    def get_user(self, request: Request) -> UserResponseModel:
        return UserResponseModel(
            username=request.user.display_name,
            user_id=request.user.user_id,
        )

    ###########################################################################

    def get_forms(self) -> t.List[FormConfigResponseModel]:
        """
        Returns a list of all forms registered with the admin.
        """
        return [
            FormConfigResponseModel(
                name=form.name, slug=form.slug, description=form.description
            )
            for form in self.forms
        ]

    def get_single_form(self, form_slug: str) -> FormConfigResponseModel:
        """
        Returns the FormConfig for the given form.
        """
        form = self.form_config_map.get(form_slug, None)
        if form is None:
            raise HTTPException(status_code=404, detail="No such form found")
        else:
            return FormConfigResponseModel(
                name=form.name,
                slug=form.slug,
                description=form.description,
            )

    def get_single_form_schema(self, form_slug: str) -> t.Dict[str, t.Any]:
        form_config = self.form_config_map.get(form_slug)

        if form_config is None:
            raise HTTPException(status_code=404, detail="No such form found")
        else:
            return form_config.pydantic_model.schema()

    async def post_single_form(
        self, request: Request, form_slug: str
    ) -> JSONResponse:
        form_config = self.form_config_map.get(form_slug)
        data = await request.json()

        if form_config is None:
            raise HTTPException(status_code=404, detail="No such form found")

        try:
            model_instance = form_config.pydantic_model(**data)
        except ValidationError as exception:
            return JSONResponse(
                {"message": json.loads(exception.json())}, status_code=400
            )

        try:
            endpoint = form_config.endpoint
            if inspect.iscoroutinefunction(endpoint):
                response = await endpoint(  # type: ignore
                    request, model_instance
                )
            else:
                response = endpoint(request, model_instance)
        except ValueError as exception:
            return JSONResponse({"message": str(exception)}, status_code=400)

        message = (
            response if isinstance(response, str) else "Successfully submitted"
        )
        return JSONResponse({"message": message})

    ###########################################################################

    def get_meta(self) -> MetaResponseModel:
        return MetaResponseModel(
            piccolo_admin_version=PICCOLO_ADMIN_VERSION,
            site_name=self.site_name,
        )

    ###########################################################################

    def get_table_list(self) -> t.List[str]:
        """
        Returns a list of all tables registered with the admin.
        """
        return [i.table_class._meta.tablename for i in self.table_configs]


def get_all_tables(
    tables: t.Sequence[t.Type[Table]],
) -> t.Sequence[t.Type[Table]]:
    """
    Fetch any related tables, and include them.
    """
    output: t.List[t.Type[Table]] = []

    def get_references(table: t.Type[Table]):
        references: t.List[t.Union[t.Type[Table], t.Any]] = [
            i._foreign_key_meta.references
            for i in table._meta.foreign_key_columns
        ]
        for reference in references:
            table = (
                reference.resolve()
                if isinstance(reference, LazyTableReference)
                else reference
            )

            if table not in output:
                output.append(table)
                get_references(table)

    for table in tables:
        if table not in output:
            output.append(table)
        get_references(table)

    return output


def create_admin(
    tables: t.Sequence[t.Union[t.Type[Table], TableConfig]],
    forms: t.List = [],
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
        table_config_map: t.Dict[t.Type[Table], t.Optional[TableConfig]] = {}

        for i in tables:
            if isinstance(i, TableConfig):
                table_config_map[i.table_class] = i
            else:
                table_config_map[i] = None

        all_table_classes = get_all_tables(tuple(table_config_map.keys()))

        all_table_classes_with_configs: t.List[
            t.Union[t.Type[Table], TableConfig]
        ] = []
        for i in all_table_classes:
            table_config = table_config_map.get(i)
            if table_config:
                all_table_classes_with_configs.append(table_config)
            else:
                all_table_classes_with_configs.append(i)

        tables = all_table_classes_with_configs

    return ExceptionMiddleware(
        CSRFMiddleware(
            AdminRouter(
                *tables,
                forms=forms,
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
