from unittest import TestCase

from piccolo.apps.user.tables import BaseUser
from piccolo.columns.column_types import (
    ForeignKey,
    Integer,
    Text,
    Timestamp,
    Varchar,
)
from piccolo.table import Table
from piccolo_api.session_auth.tables import SessionsBase
from starlette.testclient import TestClient

from piccolo_admin.endpoints import TableConfig, get_all_tables
from piccolo_admin.example import APP
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


class TestAdminRouter(TestCase):
    def test_get_meta(self):
        client = TestClient(APP)

        response = client.get("/meta/")
        self.assertEqual(
            response.json(),
            {
                "piccolo_admin_version": __VERSION__,
                "site_name": "Piccolo Admin",
                "default_language": "english",
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


class TestForms(TestCase):
    credentials = {"username": "Bob", "password": "bob123"}

    def setUp(self):
        SessionsBase.create_table(if_not_exists=True).run_sync()
        BaseUser.create_table(if_not_exists=True).run_sync()
        BaseUser(
            **self.credentials, active=True, admin=True, superuser=True
        ).save().run_sync()

    def tearDown(self):
        SessionsBase.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()

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
            "/auth/login/",
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
                    "name": "Business email form",
                    "slug": "business-email-form",
                    "description": "Send an email to a business associate.",
                },
                {
                    "name": "Booking form",
                    "slug": "booking-form",
                    "description": "Make a booking for a customer.",
                },
            ],
        )

        #######################################################################
        # Now get the schema for a form

        response = client.get("/api/forms/business-email-form/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "title": "BusinessEmailModel",
                "type": "object",
                "properties": {
                    "email": {"title": "Email", "type": "string"},
                    "title": {
                        "default": "Enquiry",
                        "title": "Title",
                        "type": "string",
                    },
                    "content": {"title": "Content", "type": "string"},
                },
                "required": ["email", "content"],
            },
        )
        response = client.get("/api/forms/email-form/schema/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"detail":"No such form found"}')

        #######################################################################
        # Now get the FormConfig for a single form

        response = client.get("/api/forms/business-email-form/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "name": "Business email form",
                "slug": "business-email-form",
                "description": "Send an email to a business associate.",
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
            "/auth/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Post a form

        form_payload = {
            "email": "director@director.com",
            "title": "Hello director",
            "content": "Hello from Piccolo Admin",
        }

        response = client.post(
            "/api/forms/business-email-form/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Email sent"})

        #######################################################################
        # Make sure async endpoints also work.

        form_payload = {
            "email": "customer@test.com",
            "name": "Bob Jones",
            "notes": "1 ticket",
        }

        response = client.post(
            "/api/forms/booking-form/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Booking complete"})

    def test_post_form_fail(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/auth/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )
        #######################################################################
        # Post a form with errors

        form_payload = {
            "email": "director",
            "title": "Hello director",
            "content": "Hello from Piccolo Admin",
        }

        response = client.post(
            "/api/forms/business-email-form/",
            json=form_payload,
            headers={"X-CSRFToken": csrftoken},
        )

        self.assertEqual(response.status_code, 400)


class TestTables(TestCase):
    credentials = {"username": "Bob", "password": "bob123"}

    def setUp(self):
        SessionsBase.create_table(if_not_exists=True).run_sync()
        BaseUser.create_table(if_not_exists=True).run_sync()
        BaseUser(
            **self.credentials, active=True, admin=True, superuser=True
        ).save().run_sync()

    def tearDown(self):
        SessionsBase.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()

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
            "/auth/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        #######################################################################
        # List all tables

        response = client.get("/api/tables/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["movie", "director", "studio"],
        )

    def test_get_user(self):
        """
        Make sure the authenticaded user can be retrieved.
        """
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/auth/login/",
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

    def test_get_language(self):
        client = TestClient(APP)

        # To get a CSRF cookie
        response = client.get("/")
        csrftoken = response.cookies["csrftoken"]

        # Login
        payload = dict(csrftoken=csrftoken, **self.credentials)
        client.post(
            "/auth/login/",
            json=payload,
            headers={"X-CSRFToken": csrftoken},
        )

        response = client.get("/api/languages/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["english"]["language"], "english")

        response = client.get("/api/languages/english/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["language"], "english")
