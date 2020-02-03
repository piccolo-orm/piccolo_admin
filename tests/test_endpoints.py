from unittest import TestCase

from piccolo_admin.endpoints import get_all_tables
from piccolo.table import Table
from piccolo.columns.column_types import ForeignKey, Varchar


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
