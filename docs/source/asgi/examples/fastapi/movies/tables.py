from piccolo.columns.column_types import ForeignKey, Varchar
from piccolo.table import Table


class Director(Table):
    name = Varchar()


class Movie(Table):
    title = Varchar()
    director = ForeignKey(Director)
