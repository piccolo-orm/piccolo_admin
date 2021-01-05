"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import os
import sys

from piccolo_api.session_auth.tables import SessionsBase
from piccolo.engine.sqlite import SQLiteEngine
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

from piccolo_admin.endpoints import create_admin
from piccolo_admin.example_data import DIRECTORS, MOVIES


DB_PATH = os.path.join(os.path.dirname(__file__), "example.sqlite")
DB = SQLiteEngine(path=DB_PATH)


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, db=DB, tablename="piccolo_user"):
    pass


class Director(Table, db=DB):
    name = Varchar(length=300, null=False)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Movie(Table, db=DB):
    name = Varchar(length=300)
    rating = Real()
    duration = Interval()
    director = ForeignKey(references=Director)
    oscar_nominations = Integer()
    won_oscar = Boolean()
    description = Text()
    release_date = Timestamp()
    box_office = Numeric(digits=(5, 1))


APP = create_admin([Director, Movie], auth_table=User, session_table=Sessions)


def populate_data():
    # Recreate the database
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)
    Director.create_table().run_sync()
    Movie.create_table().run_sync()
    User.create_table().run_sync()
    Sessions.create_table().run_sync()

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


def main(persist=False, read_only_db=False, use_hypercorn=False):
    """
    If persist is set to True, we don't rebuild all of the data each time.

    If read_only is set to True, the database will be opened in read_only
    mode. Make sure use_hypercorn is also True.
    """
    if not persist:
        populate_data()

    if read_only_db:
        DB.connection_kwargs.update(
            {"uri": True, "database": f"file:{DB_PATH}?mode=ro"}
        )

    # Server
    if use_hypercorn:
        import asyncio
        from hypercorn.asyncio import serve
        from hypercorn.config import Config

        class CustomConfig(Config):
            use_reloader = True

        asyncio.run(serve(APP, CustomConfig()))
    else:
        # Uvicorn (v0.8) doesn't support breakpoints when using auto reload.
        import uvicorn

        uvicorn.run("piccolo_admin.example:APP", reload=True, debug=True)


if __name__ == "__main__":
    args = sys.argv
    persist = "--persist" in args
    read_only_db = "--read-only-db" in args
    use_hypercorn = "--hypercorn" in args
    main(
        persist=persist,
        read_only_db=read_only_db,
        use_hypercorn=use_hypercorn,
    )
