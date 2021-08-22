from unittest import TestCase

from piccolo.columns.column_types import ForeignKey, Varchar
from piccolo.table import Table
from starlette.testclient import TestClient

from piccolo_admin.endpoints import get_all_tables
from piccolo_admin.sandbox import APP
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


class TestAdminRouter(TestCase):
    def test_get_meta(self):
        client = TestClient(APP)

        response = client.get("/meta/")
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

    def test_get_user(self):
        client = TestClient(APP)

        response = client.get("/api/user/")
        self.assertEqual(response.json(), {"error": "Auth failed"})
        self.assertEqual(response.status_code, 401)
