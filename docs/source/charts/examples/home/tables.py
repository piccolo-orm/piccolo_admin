from piccolo.columns.column_types import Varchar, ForeignKey
from piccolo.table import Table

class Director(Table):
    name = Varchar()

class Movie(Table):
    title = Varchar()
    director = ForeignKey(references=Director)