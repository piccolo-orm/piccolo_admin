from piccolo.columns.column_types import Varchar
from piccolo.table import Table


class Task(Table):
    title = Varchar()
