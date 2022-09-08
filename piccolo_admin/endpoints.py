"""
Creates a basic wrapper around a Piccolo model, turning it into an ASGI app.
"""
from __future__ import annotations

import inspect
import itertools
import json
import os
import typing as t
from dataclasses import dataclass
from datetime import timedelta
from functools import partial

from fastapi import FastAPI, File, Form, UploadFile
from piccolo.apps.user.tables import BaseUser
from piccolo.columns.base import Column
from piccolo.columns.reference import LazyTableReference
from piccolo.table import Table
from piccolo.utils.warnings import Level, colored_warning
from piccolo_api.change_password.endpoints import change_password
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.crud.hooks import Hook
from piccolo_api.crud.validators import Validators
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper
from piccolo_api.media.base import MediaStorage
from piccolo_api.media.local import LocalMediaStorage
from piccolo_api.openapi.endpoints import swagger_ui
from piccolo_api.rate_limiting.middleware import (
    InMemoryLimitProvider,
    RateLimitingMiddleware,
    RateLimitProvider,
)
from piccolo_api.session_auth.endpoints import session_login, session_logout
from piccolo_api.session_auth.middleware import SessionsAuthBackend
from piccolo_api.session_auth.tables import SessionsBase
from pydantic import BaseModel, Field, ValidationError
from starlette.exceptions import ExceptionMiddleware, HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from .translations.data import TRANSLATIONS
from .translations.models import (
    Translation,
    TranslationListItem,
    TranslationListResponse,
)
from .version import __VERSION__ as PICCOLO_ADMIN_VERSION

ASSET_PATH = os.path.join(os.path.dirname(__file__), "dist")


class UserResponseModel(BaseModel):
    username: str
    user_id: str


class MetaResponseModel(BaseModel):
    piccolo_admin_version: str
    site_name: str


class StoreFileResponseModel(BaseModel):
    file_key: str = Field(description="For example `my_file-some-uuid.jpeg`.")


class GenerateFileURLRequestModel(BaseModel):
    column_name: str
    table_name: str
    file_key: str = Field(description="For example `my_file-some-uuid.jpeg`.")


class GenerateFileURLResponseModel(BaseModel):
    file_url: str = Field(description="A URL which the file is accessible on.")


@dataclass
class TableConfig:
    """
    Gives the user more control over how a ``Table`` appears in the UI.

    :param table_class:
        The :class:`Table <piccolo.table.Table>` class to configure.
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
    :param rich_text_columns:
        You can specify ``rich_text_columns`` if you want a WYSIWYG editor
        on certain Piccolo :class:`Text <piccolo.columns.column_types.Text>`
        columns. Any columns not specified will use a standard HTML textarea
        tag in the UI.
    :param hooks:
        These are passed directly to
        :class:`PiccoloCRUD <piccolo_api.crud.endpoints>`, which powers Piccolo
        Admin under the hood. It allows you to run custom logic when a row
        is modified.
    :param media_storage:
        These columns will be used to store media. We don't directly store the
        media in the database, but instead store a string, which is a unique
        identifier, and can be used to retrieve a URL for accessing the file.
        Piccolo Admin automatically renders a file upload widget for each media
        column in the UI.

    """

    table_class: t.Type[Table]
    visible_columns: t.Optional[t.List[Column]] = None
    exclude_visible_columns: t.Optional[t.List[Column]] = None
    visible_filters: t.Optional[t.List[Column]] = None
    exclude_visible_filters: t.Optional[t.List[Column]] = None
    rich_text_columns: t.Optional[t.List[Column]] = None
    hooks: t.Optional[t.List[Hook]] = None
    media_storage: t.Optional[t.Sequence[MediaStorage]] = None

    def __post_init__(self):
        if self.visible_columns and self.exclude_visible_columns:
            raise ValueError(
                "Only specify `visible_columns` or "
                "`exclude_visible_columns`."
            )

        if self.visible_filters and self.exclude_visible_filters:
            raise ValueError(
                "Only specify `visible_filters` or `exclude_visible_filters`."
            )

        # Create a mapping for faster lookups
        self.media_columns = (
            {i.column: i for i in self.media_storage}
            if self.media_storage
            else None
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

    def get_rich_text_columns_names(self) -> t.Tuple[str, ...]:
        return (
            tuple(i._meta.name for i in self.rich_text_columns)
            if self.rich_text_columns
            else ()
        )

    def get_media_columns_names(self) -> t.Tuple[str, ...]:
        return (
            tuple(i._meta.name for i in self.media_columns)
            if self.media_columns
            else ()
        )


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
            message: str = "hello world"


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
        [Request, BaseModel],
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


def superuser_validators(piccolo_crud: PiccoloCRUD, request: Request):
    """
    We need to provide extra validation on certain tables (e.g. user and
    sessions), so only superusers can perform certain actions, otherwise the
    security of the application can be compromised.
    """
    user: BaseUser = request.user.user
    if user.superuser:
        return
    if request.method.upper() in ["PUT", "PATCH", "DELETE", "POST"]:
        raise HTTPException(
            status_code=405,
            detail="Only superusers can perform these actions.",
        )


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
        default_language_code: str = "auto",
        translations: t.List[Translation] = None,
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
        self.table_config_map = {
            table_config.table_class._meta.tablename: table_config
            for table_config in table_configs
        }

        #######################################################################
        # Make sure columns are configured properly.

        for table_config in table_configs:
            table_class = table_config.table_class
            for column in table_class._meta.columns:
                if column._meta.secret and column._meta.required:
                    message = (
                        f"{table_class._meta.tablename}."
                        f"{column._meta._name} is using `secret` and "
                        f"`required` column args which are incompatible. "
                        f"You may encounter unexpected behavior when using "
                        f"this table within Piccolo Admin."
                    )
                    colored_warning(message, level=Level.high)

        #######################################################################
        # Make sure media storage is configured properly.

        media_storage = [
            i
            for i in itertools.chain(
                *[
                    table_config.media_storage or []
                    for table_config in table_configs
                ]
            )
        ]

        if len(media_storage) != len(set(media_storage)):
            raise ValueError(
                "Media storage is misconfigured - multiple columns are saving "
                "to the same location."
            )

        #######################################################################

        self.default_language_code = default_language_code
        self.translations_map = {
            translation.language_code.lower(): translation
            for translation in (translations or TRANSLATIONS)
        }

        #######################################################################

        self.auth_table = auth_table
        self.site_name = site_name
        self.forms = forms
        self.read_only = read_only
        self.form_config_map = {form.slug: form for form in self.forms}

        with open(os.path.join(ASSET_PATH, "index.html")) as f:
            self.template = f.read()

        #######################################################################

        private_app = FastAPI(docs_url=None)
        private_app.mount("/docs/", swagger_ui(schema_url="../openapi.json"))

        for table_config in table_configs:
            table_class = table_config.table_class
            visible_column_names = table_config.get_visible_column_names()
            visible_filter_names = table_config.get_visible_filter_names()
            rich_text_columns_names = (
                table_config.get_rich_text_columns_names()
            )
            media_columns_names = table_config.get_media_columns_names()

            validators = (
                Validators(every=[superuser_validators])
                if table_class in (auth_table, session_table)
                else None
            )

            FastAPIWrapper(
                root_url=f"/tables/{table_class._meta.tablename}/",
                fastapi_app=private_app,
                piccolo_crud=PiccoloCRUD(
                    table=table_class,
                    read_only=read_only,
                    page_size=page_size,
                    schema_extra={
                        "visible_column_names": visible_column_names,
                        "visible_filter_names": visible_filter_names,
                        "rich_text_columns": rich_text_columns_names,
                        "media_columns": media_columns_names,
                    },
                    validators=validators,
                    hooks=table_config.hooks,
                ),
                fastapi_kwargs=FastAPIKwargs(
                    all_routes={
                        "tags": [f"{table_class._meta.tablename.capitalize()}"]
                    },
                ),
            )

        private_app.add_api_route(
            path="/tables/",
            endpoint=self.get_table_list,  # type: ignore
            methods=["GET"],
            response_model=t.List[str],
            tags=["Tables"],
        )

        private_app.add_api_route(
            path="/forms/",
            endpoint=self.get_forms,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
            response_model=t.List[FormConfigResponseModel],
        )

        private_app.add_api_route(
            path="/forms/{form_slug:str}/",
            endpoint=self.get_single_form,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
        )

        private_app.add_api_route(
            path="/forms/{form_slug:str}/schema/",
            endpoint=self.get_single_form_schema,  # type: ignore
            methods=["GET"],
            tags=["Forms"],
        )

        private_app.add_api_route(
            path="/forms/{form_slug:str}/",
            endpoint=self.post_single_form,  # type: ignore
            methods=["POST"],
            tags=["Forms"],
        )

        private_app.add_api_route(
            path="/user/",
            endpoint=self.get_user,  # type: ignore
            methods=["GET"],
            tags=["User"],
            response_model=UserResponseModel,
        )

        private_app.add_route(
            path="/change-password/",
            route=change_password(
                login_url="./../../public/login/",
                session_table=session_table,
                read_only=read_only,
            ),
            methods=["POST"],
        )

        #######################################################################
        # Media

        private_app.add_api_route(
            path="/media/",
            endpoint=self.store_file,  # type: ignore
            methods=["POST"],
            tags=["Media"],
            response_model=StoreFileResponseModel,
        )

        private_app.add_api_route(
            path="/media/generate-file-url/",
            endpoint=self.generate_file_url,  # type: ignore
            methods=["POST"],
            tags=["Media"],
            response_model=GenerateFileURLResponseModel,
        )

        for table_config in self.table_configs:
            if table_config.media_columns:
                for (
                    column,
                    media_storage,
                ) in table_config.media_columns.items():
                    if isinstance(media_storage, LocalMediaStorage):
                        private_app.mount(
                            path=f"/media-files/{column._meta.table._meta.tablename}/{column._meta.name}/",  # noqa: E501
                            app=StaticFiles(
                                directory=media_storage.media_path
                            ),
                        )

        #######################################################################

        public_app = FastAPI(docs_url=None)
        public_app.mount("/docs/", swagger_ui(schema_url="../openapi.json"))

        if not rate_limit_provider:
            rate_limit_provider = InMemoryLimitProvider(
                limit=1000, timespan=300
            )

        public_app.mount(
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

        public_app.add_route(
            path="/logout/",
            route=session_logout(session_table=session_table),
            methods=["POST"],
        )

        # We make the meta endpoint available without auth, because it contains
        # the site name.
        public_app.add_api_route(
            "/meta/", endpoint=self.get_meta, tags=["Meta"]  # type: ignore
        )

        # The translations are public, because we need them on the login page.
        public_app.add_api_route(
            "/translations/",
            endpoint=self.get_translation_list,  # type: ignore
            methods=["GET"],
            tags=["Translations"],
            response_model=TranslationListResponse,
        )

        public_app.add_api_route(
            "/translations/{language_code:str}/",
            endpoint=self.get_translation,  # type: ignore
            methods=["GET"],
            tags=["Translations"],
            response_model=Translation,
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

        self.mount(path="/api", app=auth_middleware(private_app))
        self.mount(path="/public", app=public_app)

    async def get_root(self, request: Request) -> HTMLResponse:
        return HTMLResponse(self.template)

    ###########################################################################

    def _get_media_storage(
        self, table_name: str, column_name: str
    ) -> MediaStorage:
        """
        Retrieve the ``MediaStorage`` for the given column.

        :raises HTTPException:
            If a matching ``MediaStorage`` can't be found.

        """
        table_config = self.table_config_map.get(table_name)
        if not table_config:
            raise HTTPException(status_code=404, detail="No such table found.")

        media_columns = table_config.media_columns

        if media_columns is None:
            raise HTTPException(
                status_code=422,
                detail="No media columns are configured for this table.",
            )

        try:
            column = table_config.table_class._meta.get_column_by_name(
                column_name
            )
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="No such column found.",
            )

        media_storage = media_columns.get(column)

        if not media_storage:
            raise HTTPException(
                status_code=422,
                detail="This column is not configured as a media_column.",
            )

        return media_storage

    async def store_file(
        self,
        request: Request,
        table_name: str = Form(None),
        column_name: str = Form(None),
        file: UploadFile = File(...),
    ) -> StoreFileResponseModel:
        """
        Stores in the file in the configured ``MediaStorage``, and returns a
        unique key for identifying that file.
        """
        if self.read_only:
            raise HTTPException(
                status_code=405, detail="Running in read-only mode."
            )

        media_storage = self._get_media_storage(
            table_name=table_name, column_name=column_name
        )

        try:
            file_key = await media_storage.store_file(
                file_name=file.filename,
                file=file.file,
                user=request.user.user,
            )
        except ValueError as exception:
            raise HTTPException(status_code=422, detail=str(exception))
        return StoreFileResponseModel(file_key=file_key)

    async def generate_file_url(
        self, request: Request, model: GenerateFileURLRequestModel
    ) -> GenerateFileURLResponseModel:
        """
        Returns a URL for accessing the given file.

        We don't use a GET for this endpoint, as using a GET param to pass the
        ``file_key`` is too restrictive on which characters can be used.
        """
        if self.read_only:
            raise HTTPException(
                status_code=405, detail="Running in read-only mode."
            )

        media_storage = self._get_media_storage(
            table_name=model.table_name, column_name=model.column_name
        )
        file_url = await media_storage.generate_file_url(
            file_key=model.file_key,
            root_url=(
                f"./api/media-files/{model.table_name}"
                f"/{model.column_name}/"
            ),
            user=request.user.user,
        )
        return GenerateFileURLResponseModel(file_url=file_url)

    ###########################################################################

    def get_user(self, request: Request) -> UserResponseModel:
        return UserResponseModel(
            username=request.user.display_name,
            user_id=request.user.user_id,
        )

    ###########################################################################
    # Custom forms

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
        """
        Handles posting of custom forms.
        """
        form_config = self.form_config_map.get(form_slug)
        data = await request.json()

        if form_config is None:
            raise HTTPException(status_code=404, detail="No such form found")

        try:
            model_instance = form_config.pydantic_model(**data)
        except ValidationError as exception:
            # We use 'detail' as it mirrors what FastAPI returns for Pydantic
            # errors, allowing us to use the same error display logic in the
            # front end.
            return JSONResponse(
                {"detail": json.loads(exception.json())}, status_code=422
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
            return JSONResponse(
                {"custom_form_error": str(exception)}, status_code=422
            )

        message = (
            response if isinstance(response, str) else "Successfully submitted"
        )
        return JSONResponse({"custom_form_success": message})

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

    ###########################################################################

    def get_translation_list(self) -> TranslationListResponse:
        """
        Return a list of language codes and names for each available
        translation.
        """
        return TranslationListResponse(
            translations=[
                TranslationListItem(
                    language_code=translation.language_code,
                    language_name=translation.language_name,
                )
                for translation in self.translations_map.values()
            ],
            default_language_code=self.default_language_code,
        )

    def get_translation(self, language_code: str = "en") -> Translation:
        """
        Return a single language. The ``language_code`` is an IETF language
        code, for example 'en' for English.
        """
        translation = self.translations_map.get(language_code.lower())
        if translation is None:
            raise HTTPException(
                status_code=404, detail="Translation not found"
            )
        return translation


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
    forms: t.List[FormConfig] = [],
    auth_table: t.Optional[t.Type[BaseUser]] = None,
    session_table: t.Optional[t.Type[SessionsBase]] = None,
    session_expiry: timedelta = timedelta(hours=1),
    max_session_expiry: timedelta = timedelta(days=7),
    increase_expiry: t.Optional[timedelta] = timedelta(minutes=20),
    page_size: int = 15,
    read_only: bool = False,
    rate_limit_provider: t.Optional[RateLimitProvider] = None,
    production: bool = False,
    site_name: str = "Piccolo Admin",
    default_language_code: str = "auto",
    translations: t.List[Translation] = None,
    auto_include_related: bool = True,
    allowed_hosts: t.Sequence[str] = [],
):
    """
    :param tables:
        Each of the tables will be added to the admin.
    :param forms:
        For each :class:`FormConfig <piccolo_admin.endpoints.FormConfig>`
        specified, a form will automatically be rendered in the user interface,
        accessible via the sidebar.
    :param auth_table:
        Either a :class:`BaseUser <piccolo.apps.user.tables.BaseUser>`, or
        ``BaseUser`` subclass table, which is used for fetching users.
        Defaults to ``BaseUser`` if none if specified.
    :param session_table:
        Either a :class:`SessionsBase <piccolo_api.session_auth.tables.SessionsBase>`,
        or ``SessionsBase`` subclass table, which is used for storing and
        querying session tokens. Defaults to ``SessionsBase`` if none if
        specified.
    :param session_expiry:
        How long a session is valid for.
    :param max_session_expiry:
        The maximum time a session is valid for, taking into account any
        refreshes using ``increase_expiry``.
    :param increase_expiry:
        If set, the ``session_expiry`` will be increased by this amount if it's
        close to expiry.
    :param page_size:
        The admin API paginates content - this sets the default number of
        results on each page.
    :param read_only:
        If ``True``, all non auth endpoints only respond to GET requests - the
        admin can still be viewed, and the data can be filtered. Useful for
        creating online demos.
    :param rate_limit_provider:
        Rate limiting middleware is used to protect the login endpoint
        against brute force attack. If not set, an
        :class:`InMemoryLimitProvider <piccolo_api.rate_limiting.middleware.InMemoryLimitProvider>`
        will be configured with reasonable defaults.
    :param production:
        If ``True``, the admin will enforce stronger security - for example,
        the cookies used will be secure, meaning they are only sent over
        HTTPS.
    :param site_name:
        Specify a different site name in the admin UI (default
        ``'Piccolo Admin'``).
    :param default_language_code:
        Specify the default language used in the admin UI. The value should be
        an `IETF language tag <https://en.wikipedia.org/wiki/IETF_language_tag>`_,
        for example ``'en'`` for English. To see available values see
        ``piccolo_admin/translations/data.py``. The UI will be automatically
        translated into this language. If a value of ``'auto'`` is specified,
        then we check the user's browser for the language they prefer, using
        the ``navigator.language`` JavaScript API.
    :param translations:
        Specify which translations are available. By default, we use every
        translation in ``piccolo_admin/translations/data.py``.

        Here's an example - if we know our users only speak English or
        Croatian, we can specify that only those translations are visible
        in the language selector in the UI::

            from piccolo.translations.data import ENGLISH, CROATIAN

            create_admin(
                tables=[TableA, TableB],
                default_language_code='hr',
                translations=[ENGLISH, CROATIAN]
            )

        You can also use this to provide your own translations, if there's a
        language we don't currently support (though please open a PR to add
        it!)::

            from piccolo.translations.models import Translation
            from piccolo.translations.data import ENGLISH

            MY_LANGUAGE = Translation(
                language_code='xx',
                language_name='My Language',
                translations={
                    'Welcome': 'XXXXX',
                    ...
                }
            )

            create_admin(
                tables=[TableA, TableB],
                default_language_code='xx',
                translations=[ENGLISH, MY_LANGUAGE]
            )

    :param auto_include_related:
        If a table has foreign keys to other tables, those tables will also be
        included in the admin by default, if not already specified. Otherwise
        the admin won't work as expected.
    :param allowed_hosts:
        This is used by the :class:`CSRFMiddleware <piccolo_api.csrf.middleware.CSRFMiddleware>`
        as an additional layer of protection when the admin is run under HTTPS.
        It must be a sequence of strings, such as ``['my_site.com']``.
    """  # noqa: E501
    auth_table = auth_table or BaseUser
    session_table = session_table or SessionsBase

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
                default_language_code=default_language_code,
                translations=translations,
            ),
            allowed_hosts=allowed_hosts,
        )
    )
