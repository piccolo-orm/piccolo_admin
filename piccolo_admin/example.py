"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import datetime
import os

from piccolo_api.session_auth.tables import SessionsBase
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.extensions.user.tables import BaseUser
from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    ForeignKey,
    Boolean,
    Text,
    Timestamp,
)

from piccolo_admin.endpoints import create_admin


USE_HYPERCORN = True


DB_PATH = os.path.join(os.path.dirname(__file__), "example.sqlite")
DB = SQLiteEngine(path=DB_PATH)


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, db=DB):
    pass


class Director(Table, db=DB):
    name = Varchar(length=300, null=False)


class Movie(Table, db=DB):
    name = Varchar(length=300)
    rating = Integer()
    director = ForeignKey(references=Director)
    won_oscar = Boolean()
    description = Text()
    release_date = Timestamp()


APP = create_admin([Director, Movie], auth_table=User, session_table=Sessions)


def main():
    # Recreate the database
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)
    Director.create_table().run_sync()
    Movie.create_table().run_sync()
    User.create_table().run_sync()
    Sessions.create_table().run_sync()

    # Add some rows
    Director(name="Peter Jackson").save().run_sync()
    director = Director(name="George Lucas")
    director.save().run_sync()
    movie = Movie(
        name="Star Wars",
        rating=100,
        director=director.id,
        description="A story from a galaxy far, far away.",
        release_date=datetime.datetime(year=1977, month=12, day=27),
    )
    movie.save().run_sync()

    # Create a user for testing login
    user = User(
        username="piccolo",
        password="piccolo123",
        admin=True,
        email="admin@test.com",
    )
    user.save().run_sync()

    # Server
    if USE_HYPERCORN:
        import asyncio
        from hypercorn.asyncio import serve
        from hypercorn.config import Config

        class CustomConfig(Config):
            use_reloader = True

        asyncio.run(serve(APP, CustomConfig()))
    else:
        # Uvicorn (v0.8) doesn't support breakpoints when using auto reload,
        # which is why Hypercorn is used by default.
        import uvicorn

        uvicorn.run("piccolo_admin.example:APP", reload=True)


if __name__ == "__main__":
    main()
