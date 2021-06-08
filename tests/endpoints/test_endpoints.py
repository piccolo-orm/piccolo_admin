from unittest import TestCase

from piccolo_admin.endpoints import create_admin, get_all_tables
from piccolo.table import Table
from piccolo.columns.column_types import ForeignKey, Varchar
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase
from starlette.testclient import TestClient


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


class TestChangeUserPassword(TestCase):

    username = "frank"
    password = "H£ll0Wo3rlD"

    def setUp(self):
        for _Table in (TableA, SessionsBase, BaseUser):
            _Table.create_table(if_not_exists=True).run_sync()

        BaseUser(
            username=self.username,
            password=self.password,
            admin=True,
            active=True,
        ).save().run_sync()

    def tearDown(self):
        for _Table in (TableA, SessionsBase, BaseUser):
            _Table.alter().drop_table(if_exists=True).run_sync()

    def test_change_user_password(self):
        """
        Make sure a user's password can be changed successfully via the API.
        """
        app = create_admin(tables=[TableA])
        client = TestClient(app=app)

        # Get a CSRF token
        home_response = client.get("/")
        csrftoken = home_response.cookies.get("csrftoken")

        # Create a session
        login_response = client.post(
            "/auth/login/",
            data={"username": self.username, "password": self.password},
            headers={"X-CSRFToken": csrftoken},
        )

        # Change password
        new_password = "Pa$$w0Rd!"
        response = client.post(
            "/api/change-password/",
            json={"username": self.username, "password": new_password},
            headers={"X-CSRFToken": csrftoken},
            cookies={"id": login_response.cookies.get("id")},
        )

        self.assertEqual(response.status_code, 200)

        # Make sure the password has been changed.
        self.assertTrue(
            BaseUser.login_sync(username=self.username, password=new_password)
            is not None
        )

    def test_auth_required(self):
        """
        Make sure the change password endpoint requires auth.
        """
        app = create_admin(tables=[TableA])
        client = TestClient(app=app)

        # Get a CSRF token
        home_response = client.get("/")
        csrftoken = home_response.cookies.get("csrftoken")

        # Try changing the password, without a valid session
        response = client.post(
            "/api/change-password/",
            json={"username": self.username, "password": "Pa$$w0Rd!"},
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertTrue(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "Auth failed"})
