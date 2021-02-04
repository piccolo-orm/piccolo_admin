"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import asyncio
import os
import typing as t

from hypercorn.asyncio import serve
from hypercorn.config import Config
from piccolo_api.session_auth.tables import SessionsBase
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.engine.postgres import PostgresEngine
from piccolo.apps.user.tables import BaseUser
from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    ForeignKey,
    Boolean,
    Interval,
    Text,
    Timestamp,
    Numeric,
    Real,
)
from piccolo.columns.readable import Readable
import targ

from piccolo_admin.endpoints import create_admin
from piccolo_admin.example_data import DIRECTORS, MOVIES


class Sessions(SessionsBase):
    pass


class User(BaseUser, tablename="piccolo_user"):
    pass


class Director(Table):
    name = Varchar(length=300, null=False)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Movie(Table):
    name = Varchar(length=300)
    rating = Real()
    duration = Interval()
    director = ForeignKey(references=Director)
    oscar_nominations = Integer()
    won_oscar = Boolean()
    description = Text()
    release_date = Timestamp()
    box_office = Numeric(digits=(5, 1))


TABLE_CLASSES: t.Tuple[t.Type[Table]] = (Director, Movie, User, Sessions)
APP = create_admin([Director, Movie], auth_table=User, session_table=Sessions)


def set_engine(engine: str = "sqlite"):
    if engine == "postgres":
        db = PostgresEngine(config={"database": "piccolo_admin"})
    else:
        sqlite_path = os.path.join(os.path.dirname(__file__), "example.sqlite")
        db = SQLiteEngine(path=sqlite_path)

    for table_class in TABLE_CLASSES:
        table_class._meta._db = db


def create_schema(persist: bool = False):
    if not persist:
        for table_class in reversed(TABLE_CLASSES):
            table_class.alter().drop_table(if_exists=True).run_sync()

    for table_class in TABLE_CLASSES:
        table_class.create_table(if_not_exists=True).run_sync()


def populate_data():
    # Add some rows
    Director.insert(*[Director(**d) for d in DIRECTORS]).run_sync()
    Movie.insert(*[Movie(**m) for m in MOVIES]).run_sync()

    # Create a user for testing login
    user = User(
        username="piccolo",
        password="piccolo123",
        admin=True,
        email="admin@test.com",
    )
    user.save().run_sync()


def run(
    persist: bool = False, engine: str = "sqlite",
):
    """
    Start the Piccolo admin.

    :param persist:
        If True, we don't rebuild all of the data each time.
    :param engine:
        Options are sqlite and postgres. By default sqlite is used.

    """
    set_engine(engine)
    create_schema(persist=persist)

    if not persist:
        populate_data()

    # Server
    class CustomConfig(Config):
        use_reloader = True
        accesslog = "-"

    asyncio.run(serve(APP, CustomConfig()))


if __name__ == "__main__":
    cli = targ.CLI(description="Piccolo Admin")
    cli.register(run)
    cli.run(solo=True)
