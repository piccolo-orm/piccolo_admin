"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import asyncio
import datetime
import decimal
import os
import random
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
from piccolo_admin.example_data import DIRECTORS, MOVIES, MOVIE_WORDS


class Sessions(SessionsBase):
    pass


class User(BaseUser, tablename="piccolo_user"):
    pass


class Director(Table, help_text="The main director for a movie."):
    name = Varchar(length=300, null=False)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Movie(Table):
    name = Varchar(length=300)
    rating = Real(help_text="The rating on IMDB.")
    duration = Interval()
    director = ForeignKey(references=Director)
    oscar_nominations = Integer()
    won_oscar = Boolean()
    description = Text()
    release_date = Timestamp()
    box_office = Numeric(digits=(5, 1), help_text="In millions of US dollars.")


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


def populate_data(inflate: int = 0, engine: str = "sqlite"):
    """
    Populate the database with some example data.

    :param inflate:
        If set, this number of extra rows are inserted containing dummy data.
        This is useful for testing.

    """
    # Add some rows
    Director.insert(*[Director(**d) for d in DIRECTORS]).run_sync()
    Movie.insert(*[Movie(**m) for m in MOVIES]).run_sync()

    if engine == "postgres":
        # We need to update the sequence, as we explicitly set the IDs for the
        # directors we just inserted
        Director.raw(
            "SELECT setval('director_id_seq', max(id)) FROM director"
        ).run_sync()

    # Create a user for testing login
    user = User(
        username="piccolo",
        password="piccolo123",
        admin=True,
        email="admin@test.com",
    )
    user.save().run_sync()

    if inflate:
        try:
            import faker
        except ImportError:
            print(
                "Install faker to use this feature: "
                "`pip install piccolo_admin[faker]`"
            )
        else:
            fake = faker.Faker()
            remaining = inflate
            chunk_size = 100

            while remaining > 0:
                if remaining < chunk_size:
                    chunk_size = remaining
                    remaining = 0
                else:
                    remaining = remaining - chunk_size

                Director.insert(
                    *[Director(name=fake.name()) for _ in range(chunk_size)]
                ).run_sync()

                director_ids = (
                    Director.select(Director.id)
                    .order_by(Director.id, ascending=False)
                    .limit(chunk_size)
                    .output(as_list=True)
                    .run_sync()
                )

                movies = []
                for _ in range(chunk_size):
                    oscar_nominations = random.sample(
                        [0, 0, 0, 0, 0, 1, 1, 3, 5], 1
                    )[0]
                    won_oscar = oscar_nominations > 0
                    rating = (
                        random.randint(80, 100)
                        if won_oscar
                        else random.randint(1, 100)
                    ) / 10

                    movie = Movie(
                        name="{} {}".format(
                            fake.word().title(),
                            fake.word(ext_word_list=MOVIE_WORDS),
                        ),
                        rating=rating,
                        duration=datetime.timedelta(
                            minutes=random.randint(60, 210)
                        ),
                        director=random.sample(director_ids, 1)[0],
                        oscar_nominations=oscar_nominations,
                        won_oscar=won_oscar,
                        description=fake.sentence(30),
                        release_date=fake.date_time(),
                        box_office=decimal.Decimal(
                            str(random.randint(10, 1500) / 10)
                        ),
                    )
                    movies.append(movie)

                Movie.insert(*movies).run_sync()


def run(persist: bool = False, engine: str = "sqlite", inflate: int = 0):
    """
    Start the Piccolo admin.

    :param persist:
        If True, we don't rebuild all of the data each time.
    :param engine:
        Options are sqlite and postgres. By default sqlite is used.
    :param inflate:
        If set, this number of extra rows are inserted containing dummy data.
        This is useful when you need to test with lots of data. Example
        `--inflate=10000`.

    """
    set_engine(engine)
    create_schema(persist=persist)

    if not persist:
        populate_data(inflate=inflate, engine=engine)

    # Server
    class CustomConfig(Config):
        use_reloader = True
        accesslog = "-"

    asyncio.run(serve(APP, CustomConfig()))


if __name__ == "__main__":
    cli = targ.CLI(description="Piccolo Admin")
    cli.register(run)
    cli.run(solo=True)
