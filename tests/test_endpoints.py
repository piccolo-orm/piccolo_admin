import csv
import datetime
import io
import os
import uuid
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from piccolo.apps.user.tables import BaseUser
from piccolo.columns.column_types import (
    ForeignKey,
    Integer,
    Text,
    Timestamp,
    Varchar,
)
from piccolo.table import Table, create_db_tables_sync, drop_db_tables_sync
from piccolo.testing.test_case import TableTest
from piccolo_api.crud.hooks import Hook, HookType
from piccolo_api.crud.validators import Validators
from piccolo_api.media.local import LocalMediaStorage
from piccolo_api.mfa.authenticator.tables import AuthenticatorSecret
from piccolo_api.session_auth.tables import SessionsBase
from starlette.exceptions import HTTPException
from starlette.testclient import TestClient

from piccolo_admin.endpoints import (
    OrderBy,
    TableConfig,
    create_admin,
    get_all_tables,
)
from piccolo_admin.example.app import APP, MEDIA_ROOT, Director, Movie
from piccolo_admin.translations.data import ENGLISH, FRENCH, TRANSLATIONS
from piccolo_admin.version import __VERSION__


class TableA(Table):
    name = Varchar(length=100)


class TableB(Table):
    table_a = ForeignKey(TableA)


class TableC(Table):
    table_b = ForeignKey(TableB)


class TestGetAllTables(TestCase):
    def test_all_returned(self):
        tables = get_all_tables([TableC])
        self.assertEqual(tables, [TableC, TableB, TableA])


class Post(Table):
    name = Varchar(length=100)
    content = Text()
    created = Timestamp()
    rating = Integer()


class TestTableConfig(TestCase):
    def test_visible_columns(self):
        post_table = TableConfig(
            table_class=Post,
            visible_columns=[Post._meta.primary_key, Post.name],
        )
        self.assertEqual(
            post_table.get_visible_column_names(),
            ("id", "name"),
        )

    def test_exclude_visible_columns(self):
        post_table = TableConfig(
            table_class=Post,
            exclude_visible_columns=[Post._meta.primary_key, Post.name],
        )
        self.assertEqual(
            tuple(i._meta.name for i in post_table.get_visible_columns()),
            ("content", "created", "rating"),
        )

    def test_exclude_visible_columns_without_pk(self):
        post_table = TableConfig(
            table_class=Post,
            exclude_visible_columns=[Post.name],
        )
        self.assertEqual(
            tuple(i._meta.name for i in post_table.get_visible_columns()),
            ("id", "content", "created", "rating"),
        )

    def test_visible_exclude_columns_error(self):
        with self.assertRaises(ValueError):
            post_table = TableConfig(
                table_class=Post,
                visible_columns=[Post._meta.primary_key, Post.name],
                exclude_visible_columns=[Post._meta.primary_key],
            )
            post_table.get_visible_columns()

    def test_visible_filters(self):
        post_table = TableConfig(
            table_class=Post,
            visible_filters=[Post.name, Post.rating],
        )
        self.assertEqual(
            post_table.get_visible_filter_names(),
            ("name", "rating"),
        )

    def test_exclude_visible_filters(self):
        post_table = TableConfig(
            table_class=Post,
            exclude_visible_filters=[Post._meta.primary_key, Post.name],
        )
        self.assertEqual(
            tuple(i._meta.name for i in post_table.get_visible_filters()),
            ("content", "created", "rating"),
        )

    def test_visible_filters_error(self):
        with self.assertRaises(ValueError):
            post_table = TableConfig(
                table_class=Post,
                visible_filters=[Post.name],
                exclude_visible_filters=[Post.name, Post.rating],
            )
            post_table.get_visible_filters()

    def test_link_column(self):
        """
        Make sure the custom `link_column` is returned.
        """
        config = TableConfig(
            table_class=Post,
            link_column=Post.name,
        )
        self.assertIs(config.get_link_column(), Post.name)

    def test_link_column_default(self):
        """
        Make sure the `link_column` defaults to the primary key.
        """
        config = TableConfig(table_class=Post)
        self.assertIs(config.get_link_column(), Post._meta.primary_key)

    def test_link_column_error(self):
        """
        Make sure foreign key columns aren't allowed as the `link_column`.
        """
        with self.assertRaises(ValueError):
            TableConfig(
                table_class=TableB,
                link_column=TableB.table_a,
            )

    def test_sort_column(self):
        """
        Make sure the custom `sort_column` is returned.
        """
        config = TableConfig(
            table_class=Post,
            order_by=[OrderBy(Post.name)],
        )
        self.assertIs(config.get_order_by()[0].column, Post.name)

    def test_sort_column_default(self):
        """
        Make sure the `sort_column` defaults to the primary key.
        """
        config = TableConfig(table_class=Post)
        self.assertIs(config.get_order_by()[0].column, Post._meta.primary_key)

    def test_time_resolution(self):
        """
        Make sure `time_resolution` is returned.
        """
        config = TableConfig(
            table_class=Post,
            time_resolution={Post.created: 1},
        )
        self.assertDictEqual(config.get_time_resolution(), {"created": 1})


class TestAdminRouter(TestCase):
    def test_init(self):
        with self.assertRaises(ValueError) as manager:
            create_admin(
                tables=[
                    TableConfig(
                        Movie,
                        media_storage=[
                            LocalMediaStorage(
                                column=Movie.poster, media_path="/tmp/"
                            )
                        ],
                    ),
                    TableConfig(
                        Director,
                        media_storage=[
                            LocalMediaStorage(
                                column=Movie.screenshots, media_path="/tmp/"
                            )
                        ],
                    ),
                ]
            )
        self.assertEqual(
            str(manager.exception),
            "Media storage is misconfigured - multiple columns are saving "
            "to the same location.",
        )

    def test_get_meta(self):
        client = TestClient(APP)

        response = client.get("/public/meta/")
        self.assertEqual(
            response.json(),
            {
                "piccolo_admin_version": __VERSION__,
                "site_name": "Piccolo Admin",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_get_root(self):
        client = TestClient(APP)

        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_auth_exception(self):
        client = TestClient(APP)

        response = client.get("/api/user/")
        self.assertEqual(response.json(), {"error": "Auth failed"})
        self.assertEqual(response.status_code, 401)

        response = client.get("/api/change-password/")
        self.assertEqual(response.json(), {"error": "Auth failed"})
        self.assertEqual(response.status_code, 401)


class TestForms(TableTest):
    credentials = {"username": "Bob", "password": "bob123"}

    tables = [BaseUser, SessionsBase, AuthenticatorSecret, Movie, Director]

    def setUp(self):
        super().setUp()
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    def test_forms(self):
        """
        Make sure the form listing can be retrieved, and the schema for a form.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        #######################################################################
        # List all forms

        response = client.get("/api/forms/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "name": "Calculator",
                    "slug": "calculator",
                    "description": "Adds two numbers together.",
                },
                {
                    "name": "Download director movies",
                    "slug": "download-director-movies",
                    "description": (
                        "Download a list of movies for the director as a CSV "
                        "file."
                    ),
                },
                {
                    "name": "Booking form",
                    "slug": "booking-form",
                    "description": "Make a booking for a customer.",
                },
                {
                    "name": "Download schedule",
                    "slug": "download-schedule",
                    "description": "Download the schedule for the day.",
                },
            ],
        )

        #######################################################################
        # Now get the schema for a form

        response = client.get("/api/forms/booking-form/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "properties": {
                    "email": {
                        "format": "email",
                        "title": "Email",
                        "type": "string",
                    },
                    "movie": {
                        "default": "Star Wars: Episode IV - A New Hope",
                        "title": "Movie",
                        "type": "string",
                    },
                    "name": {"title": "Name", "type": "string"},
                    "notes": {
                        "default": "N/A",
                        "title": "Notes",
                        "type": "string",
                    },
                    "starts_at": {
                        "format": "date-time",
                        "title": "Starts At",
                        "type": "string",
                    },
                    "tickets": {"title": "Tickets", "type": "integer"},
                },
                "required": ["email", "name", "tickets", "starts_at"],
                "title": "BookingModel",
                "type": "object",
            },
        )
        response = client.get("/api/forms/email-form/schema/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"detail":"No such form found"}')

        #######################################################################
        # Now get the FormConfig for a single form

        response = client.get("/api/forms/booking-form/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            {
                "name": "Booking form",
                "slug": "booking-form",
                "description": "Make a booking for a customer.",
            },
        )
        response = client.get("/api/forms/no-such-form/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"detail":"No such form found"}')

    def test_post_form_success(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Post a form

        form_payload = {
            "email": "customer@example.com",
            "name": "Alice Jones",
            "tickets": 2,
            "starts_at": datetime.datetime.now().isoformat(),
        }

        response = client.post(
            "/api/forms/booking-form/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"custom_form_success": "Booking complete"}
        )

    def test_image_response(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Post a form

        form_payload = {
            "director_name": "George Lucas",
        }

        response = client.post(
            "/api/forms/download-director-movies/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 200)

        headers = response.headers

        self.assertEqual(
            headers["content-disposition"],
            'attachment; filename="director_movies.csv"',
        )

        self.assertEqual(
            headers["content-type"],
            "text/csv; charset=utf-8",
        )

        reader = csv.reader(io.StringIO(response.content.decode()))
        rows = [i for i in reader]
        self.assertListEqual(rows[0], ["name", "release_date"])

    def test_post_form_fail(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Post a form with errors

        form_payload = {
            "email": "customer",  # This is incorrect
            "name": "Alice Jones",
            "tickets": 2,
            "starts_at": datetime.datetime.now().isoformat(),
        }

        response = client.post(
            "/api/forms/booking-form/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 422)


class TestSidebarLinks(TableTest):
    credentials = {"username": "Bob", "password": "bob123"}

    tables = [BaseUser, SessionsBase, AuthenticatorSecret]

    def setUp(self):
        super().setUp()
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    def test_sidebar_links(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Get sidebar links

        response = client.get("/api/links/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "Top Movies": "/#/movie?__order=-box_office",
                "Google": "https://google.com",
            },
        )


class TestMediaStorage(TableTest):
    credentials = {"username": "Bob", "password": "bob123"}

    tables = [BaseUser, SessionsBase, AuthenticatorSecret]

    def setUp(self):
        super().setUp()
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    @patch("piccolo_api.media.base.uuid")
    def test_image_upload(self, uuid_module: MagicMock):
        uuid_value = uuid.uuid4()
        uuid_module.uuid4.return_value = uuid_value

        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        test_file_path = os.path.join(
            os.path.dirname(__file__), "files/bulb.jpg"
        )

        with open(test_file_path, "rb") as test_file:
            response = client.post(
                "/api/media/",
                data={"table_name": "movie", "column_name": "poster"},
                files={"file": ("bulb.jpg", test_file, "image/jpeg")},
                headers={"X-CSRFToken": csrftoken},
            )

        self.assertEqual(response.status_code, 200)
        file_key: str = response.json().get("file_key")
        self.assertIsNotNone(file_key)

        # Make sure that we can retrieve the URL
        response = client.post(
            "/api/media/generate-file-url/",
            json={
                "table_name": "movie",
                "column_name": "poster",
                "file_key": file_key,
            },
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "file_url": f"./api/media-files/movie/poster"
                f"/bulb-{uuid_value}.jpg"
            },
        )

        # Remove the test file from the media directory
        Path(MEDIA_ROOT, "movie_poster", file_key).unlink()

    def test_store_file_read_only(self):
        test_file_path = os.path.join(
            os.path.dirname(__file__), "example_media"
        )

        MOVIE_POSTER_MEDIA = LocalMediaStorage(
            column=Movie.poster,
            media_path=os.path.join(test_file_path),
        )

        movie_config = TableConfig(
            table_class=Movie,
            media_storage=[MOVIE_POSTER_MEDIA],
        )

        APP = create_admin([movie_config], read_only=True)

        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        response = client.post(
            "/api/media/",
            data={"table_name": "movie", "column_name": "poster"},
            files={"file": ("bulb.jpg", b"file", "image/jpeg")},
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.content,
            b'{"detail":"Running in read-only mode."}',
        )

    def test_generate_file_url_read_only(self):
        test_file_path = os.path.join(
            os.path.dirname(__file__), "example_media"
        )

        MOVIE_POSTER_MEDIA = LocalMediaStorage(
            column=Movie.poster,
            media_path=os.path.join(test_file_path),
        )

        movie_config = TableConfig(
            table_class=Movie,
            media_storage=[MOVIE_POSTER_MEDIA],
        )

        APP = create_admin([movie_config], read_only=True)

        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        response = client.post(
            "/api/media/generate-file-url/",
            json={
                "table_name": "movie",
                "column_name": "poster",
                "file_key": "file_key",
            },
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.content,
            b'{"detail":"Running in read-only mode."}',
        )


class TestTables(TableTest):
    credentials = {"username": "Bob", "password": "bob123"}

    tables = [SessionsBase, BaseUser, AuthenticatorSecret]

    def setUp(self):
        super().setUp()
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    def test_tables(self):
        """
        Make sure the table listing can be retrieved.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        #######################################################################
        # List all tables

        response = client.get("/api/tables/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                "array_columns",
                "choices",
                "constraint_target",
                "constraints",
                "date_time_columns",
                "director",
                "movie",
                "nullable_columns",
                "required_columns",
                "sorted_columns",
                "studio",
                "ticket",
            ],
        )

    def test_tables_grouped(self):
        """
        Make sure the grouped table listing can be retrieved.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        #######################################################################
        # List all tables

        response = client.get("/api/tables/grouped/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "grouped": {
                    "Booking": ["ticket"],
                    "Movies": ["director", "movie", "studio"],
                    "Testing": [
                        "array_columns",
                        "choices",
                        "constraint_target",
                        "constraints",
                        "date_time_columns",
                        "nullable_columns",
                        "required_columns",
                        "sorted_columns",
                    ],
                },
                "ungrouped": [],
            },
        )

    def test_get_user(self):
        """
        Make sure the authenticated user can be retrieved.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        #######################################################################
        # Auth user

        response = client.get("/api/user/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"username": "Bob", "user_id": "1"},
        )

    def test_schema(self):
        """
        We add some additonal attributes to the table schema.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        # Test `Director` table
        response = client.get("/api/tables/director/schema/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["extra"]["link_column_name"], "id")
        self.assertEqual(data["extra"]["rich_text_columns"], [])
        self.assertEqual(
            data["extra"]["visible_column_names"],
            ["id", "name", "gender", "photo"],
        )
        self.assertEqual(
            data["extra"]["visible_filter_names"],
            [
                "id",
                "name",
                "years_nominated",
                "gender",
                "photo",
                "additional_skills",
            ],
        )
        self.assertEqual(data["extra"]["media_columns"], ["photo"])

        # Test the `Ticket` table, as it has `time_resolution` specified in the
        # `TableConfig`.
        response = client.get("/api/tables/ticket/schema/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertDictEqual(
            data["extra"]["time_resolution"],
            {"booked_on": 1, "start_time": 60},
        )


class TestTranslations(TestCase):
    def test_translations(self):
        """
        Test the default configuration, where the translations endpoint should
        return all translations.
        """
        client = TestClient(APP)

        response = client.get("/public/translations/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["default_language_code"], "auto")
        self.assertListEqual(
            [i["language_code"] for i in data.get("translations")],
            [i.language_code for i in TRANSLATIONS],
        )

    def test_translations_custom(self):
        """
        Test a custom configuration, where the translations endpoint should
        return only the configured translations.
        """
        translations = [ENGLISH, FRENCH]

        client = TestClient(
            create_admin(
                tables=[],
                translations=translations,
                default_language_code="fr",
            )
        )

        response = client.get("/public/translations/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["default_language_code"], "fr")
        self.assertListEqual(
            [i["language_code"] for i in data.get("translations")],
            [i.language_code for i in translations],
        )

    def test_get_single_translation(self):
        """
        Make sure we can retrieve a single translation.
        """
        client = TestClient(APP)

        response = client.get("/public/translations/en/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["translations"]["About"], "About")

    def test_get_language_case_insensitive(self):
        """
        Make sure the language codes are case insensitive. This is important,
        as most browsers use `en-US`, but older Safari versions used `en-us`.
        """
        client = TestClient(APP)

        for language_code in ("en", "EN"):
            response = client.get(f"/public/translations/{language_code}/")
            self.assertEqual(response.status_code, 200)

    def test_get_language_failed(self):
        """
        Make sure unrecognised languages are handled gracefully.
        """
        client = TestClient(APP)

        response = client.get("/public/translations/nolanguage/")
        self.assertEqual(response.status_code, 404)


class TestHooks(TestCase):
    credentials = {"username": "Bob", "password": "bob123"}

    def setUp(self):
        create_db_tables_sync(SessionsBase, BaseUser, Post, if_not_exists=True)
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    def tearDown(self):
        drop_db_tables_sync(SessionsBase, BaseUser, Post)

    def test_hooks(self):
        """
        If a hook is passed to ``TableConfig``, make sure it gets called.
        """
        mock = MagicMock()

        def hook(row, mock: MagicMock = mock):
            mock()
            row.name = "New Post 1"
            return row

        app = create_admin(
            tables=[
                TableConfig(
                    table_class=Post,
                    hooks=[Hook(hook_type=HookType.pre_save, callable=hook)],
                )
            ]
        )

        client = TestClient(app)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        # Now try creating a new row
        response = client.post(
            "/api/tables/post/",
            json={
                "name": "New Post",
                "content": "Some content",
                "rating": 100,
                "created": datetime.datetime.now().isoformat(),
            },
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 201)

        # Make sure the row is created with the correct data (the hook modified
        # the name attribute).
        self.assertFalse(
            Post.exists().where(Post.name == "New Post").run_sync()
        )
        self.assertTrue(
            Post.exists().where(Post.name == "New Post 1").run_sync()
        )

        # Make sure the hook was only called once.
        mock.assert_called_once()


class TestValidators(TestCase):
    credentials = {"username": "Bob", "password": "bob123"}

    def setUp(self):
        create_db_tables_sync(SessionsBase, BaseUser, Post, if_not_exists=True)
        BaseUser.create_user_sync(
            **self.credentials, active=True, admin=True, superuser=True
        )

    def tearDown(self):
        drop_db_tables_sync(SessionsBase, BaseUser, Post)

    def test_validators(self):
        """
        Make sure validators can be used to control access to an API endpoint.
        """

        def post_single_validator(piccolo_crud, request):
            raise HTTPException(detail="Not allowed!", status_code=403)

        app = create_admin(
            tables=[
                TableConfig(
                    Post,
                    validators=Validators(post_single=[post_single_validator]),
                ),
            ]
        )

        client = TestClient(app)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/public/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        # Make sure some requests pass
        response = client.get("/api/tables/post/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"rows": []})

        # Make sure the endpoint with validation returns an error code.
        response = client.post(
            "/api/tables/post/",
            json={"csrftoken": "csrftoken"},
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{"detail":"Not allowed!"}')
