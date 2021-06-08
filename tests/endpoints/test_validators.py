from dataclasses import dataclass
from unittest import TestCase

from piccolo_admin.endpoints import create_admin
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase
from starlette.testclient import TestClient


@dataclass
class Credentials:
    csrf_token: str
    session_token: str


NEW_USER = {}


class TestValidators(TestCase):
    password = "password123"

    def _create_superuser(self) -> BaseUser:
        user = BaseUser(
            username="superuser",
            email="superuser@example.com",
            password=self.password,
            active=True,
            superuser=True,
            admin=True,
        )
        user.save().run_sync()
        return user

    def _create_admin_user(self) -> BaseUser:
        user = BaseUser(
            username="admin",
            email="admin@example.com",
            password=self.password,
            active=True,
            superuser=False,
            admin=True,
        )
        user.save().run_sync()
        return user

    def _create_non_admin_user(self) -> BaseUser:
        user = BaseUser(
            username="non_admin",
            email="non_admin@example.com",
            password=self.password,
            active=True,
            superuser=False,
            admin=False,
        )
        user.save().run_sync()
        return user

    def _create_inactive_user(self) -> BaseUser:
        user = BaseUser(
            username="inactive",
            email="inactive@example.com",
            password=self.password,
            active=False,
            superuser=False,
            admin=False,
        )
        user.save().run_sync()
        return user

    ###########################################################################

    def setUp(self):
        for _Table in (BaseUser, SessionsBase):
            _Table.create_table(if_not_exists=True).run_sync()

        self.admin_user = self._create_admin_user()
        self.superuser = self._create_superuser()
        self.non_admin_user = self._create_non_admin_user()
        self.inactive_user = self._create_inactive_user()

    def tearDown(self):
        BaseUser.alter().drop_table(if_exists=True).run_sync()

    ###########################################################################

    def _get_credentials(
        self, client: TestClient, user: BaseUser
    ) -> Credentials:
        # Get a CSRF token
        home_response = client.get("/")
        csrf_token = home_response.cookies.get("csrftoken")

        # Create a session
        login_response = client.post(
            "/auth/login/",
            data={"username": user.username, "password": self.password},
            headers={"X-CSRFToken": csrf_token},
        )

        return Credentials(
            csrf_token=csrf_token,
            session_token=login_response.cookies.get("id"),
        )

    ###########################################################################

    def test_get_all(self):
        """
        This should work for all active admin users.
        """
        for user in (self.admin_user, self.superuser):
            app = create_admin(tables=[])
            client = TestClient(app=app)
            credentials = self._get_credentials(client=client, user=user)

            # Try fetching the data
            response = client.get(
                "/api/tables/piccolo_user",
                cookies={"id": credentials.session_token},
            )
            self.assertTrue(response.status_code, 200)

    def test_post(self):
        """
        Make sure that only superusers can create other superuser and admin
        users.

        Admin users can create other non-admin users.
        """
        # Test creating superusers
        # I need the payload for creating a new user ...
        for user in (self.admin_user, self.superuser):
            app = create_admin(tables=[])
            client = TestClient(app=app)
            credentials = self._get_credentials(client=client, user=user)

            # Try fetching the data
            response = client.post(
                "/api/tables/piccolo_user",
                cookies={"id": credentials.session_token},
            )
            self.assertTrue(response.status_code, 200)
