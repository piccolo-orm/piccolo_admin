import datetime
import decimal
import enum
import logging
import os
import random
import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo.columns.column_types import (
    JSON,
    UUID,
    Array,
    BigInt,
    Boolean,
    Date,
    Email,
    ForeignKey,
    Integer,
    Interval,
    Numeric,
    OnDelete,
    Real,
    Serial,
    SmallInt,
    Text,
    Time,
    Timestamp,
    Timestamptz,
    Varchar,
)
from piccolo.columns.readable import Readable
from piccolo.engine.postgres import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table, create_db_tables_sync, drop_db_tables_sync
from piccolo_api.mfa.authenticator.tables import (
    AuthenticatorSecret as AuthenticatorSecret_,
)
from piccolo_api.session_auth.tables import SessionsBase

from piccolo_admin.example.data import (
    DIRECTORS,
    MOVIE_WORDS,
    MOVIES,
    SORTED_COLUMNS,
    STUDIOS,
    TICKETS,
)

logger = logging.getLogger()

USERNAME = "piccolo"
PASSWORD = "piccolo123"


class Sessions(SessionsBase):
    pass


class User(BaseUser, tablename="piccolo_user"):
    pass


class AuthenticatorSecret(AuthenticatorSecret_):
    pass


class Director(Table, help_text="The main director for a movie."):
    class Gender(str, enum.Enum):
        male = "m"
        female = "f"
        non_binary = "n"

    class Skill(str, enum.Enum):
        producer = "producer"
        actor = "actor"
        director_of_photography = "director of photography"
        special_effects = "special effects"

    id: Serial
    name = Varchar(length=300, null=False)
    years_nominated = Array(
        base_column=Integer(),
        help_text=(
            "Which years this director was nominated for a best director "
            "Oscar."
        ),
    )
    gender = Varchar(length=1, choices=Gender)
    photo = Varchar()
    additional_skills = Array(
        base_column=Varchar(),
        choices=Skill,
        help_text=(
            "Additional skills which the director has besides directing."
        ),
    )

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Studio(Table, help_text="A movie studio."):
    pk = UUID(primary_key=True)
    name = Varchar(unique=True)
    facilities = JSON()
    description = Text()

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Movie(Table):
    class Genre(int, enum.Enum):
        fantasy = 1
        sci_fi = 2
        documentary = 3
        horror = 4
        action = 5
        comedy = 6
        romance = 7
        musical = 8

    id: Serial
    name = Varchar(length=300)
    rating = Real(help_text="The rating on IMDB.")
    duration = Interval()
    director = ForeignKey(references=Director)
    oscar_nominations = Integer()
    won_oscar = Boolean()
    description = Text()
    poster = Varchar()
    screenshots = Array(base_column=Varchar())
    release_date = Date(null=True)
    box_office = Numeric(digits=(5, 1), help_text="In millions of US dollars.")
    tags = Array(base_column=Varchar())
    barcode = BigInt(default=0)
    genre = SmallInt(choices=Genre, null=True)
    studio = ForeignKey(Studio)

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])


class Ticket(Table):
    id: Serial
    booked_by = Varchar(length=255)
    movie = ForeignKey(Movie)
    start_date = Date()
    start_time = Time()
    booked_on = Timestamptz(null=True, default=None)
    vip = Boolean(null=True, default=None)


###############################################################################
# Some tables which are for UI testing with Playwright.


class ArrayColumns(Table):
    varchar = Array(Varchar(64))
    integer = Array(Integer())
    email = Array(Email())
    timestamp = Array(Timestamp())
    date = Array(Date())
    time = Array(Time())


class NullableColumns(Table):
    """
    A table used for UI tests.
    """

    id: Serial
    integer = Integer(
        null=True,
        default=None,
        required=False,
    )
    real = Real(null=True, default=None)
    numeric = Numeric(null=True, default=None)
    uuid = UUID(null=True, default=None)
    email = Email(null=True, default=None)
    timestamp = Timestamp(null=True, default=None)
    date = Date(null=True, default=None)
    json_ = JSON(null=True, default=None)
    text = Text(null=True, default=None)
    varchar = Varchar(null=True, default=None)
    boolean = Boolean(null=True, default=None)


class RequiredColumns(Table):
    id: Serial
    varchar = Varchar(required=True)
    array = Array(Varchar(), required=True)


class SortedColumns(Table):
    """
    A table used for UI tests.
    """

    id: Serial
    integer = Integer()
    letter = Varchar()


class ConstraintTarget(Table):
    """
    A table used for UI tests.
    """

    id: Serial
    name = Varchar()


class Constraints(Table):
    """
    A table used for UI tests.
    """

    id: Serial
    cascade = ForeignKey(
        ConstraintTarget,
        null=True,
        default=None,
        on_delete=OnDelete.cascade,
    )
    restrict = ForeignKey(
        ConstraintTarget, null=True, default=None, on_delete=OnDelete.restrict
    )
    no_action = ForeignKey(
        ConstraintTarget,
        null=True,
        default=None,
        on_delete=OnDelete.no_action,
    )
    set_null = ForeignKey(
        ConstraintTarget, on_delete=OnDelete.set_null, null=True, default=None
    )
    set_default = ForeignKey(
        ConstraintTarget,
        on_delete=OnDelete.set_default,
        null=True,
        default=None,
    )


class DateTimeColumns(Table):
    date = Date()
    date_null = Date(null=True, default=None)
    time = Time()
    time_null = Time(null=True, default=None)
    timestamp = Timestamp()
    timestamp_null = Timestamp(null=True, default=None)
    timestamptz = Timestamptz()
    timestamptz_null = Timestamptz(null=True, default=None)


class Choices(Table):
    class ArrayChoices(enum.Enum):
        a = "a"
        b = "b"
        c = "c"

    class DateChoices(enum.Enum):
        early = datetime.date(year=2000, month=1, day=1)
        late = datetime.date(year=2020, month=1, day=1)

    class IntegerChoices(enum.Enum):
        low = 1
        medium = 2
        high = 3

    class VarcharChoices(enum.Enum):
        a = "a"
        b = "b"
        c = "c"

    array = Array(base_column=Varchar(), choices=ArrayChoices)
    array_null = Array(base_column=Varchar(), choices=ArrayChoices, null=True)
    date = Date(choices=DateChoices)
    date_null = Date(choices=DateChoices, null=True)
    integer = Integer(choices=IntegerChoices)
    integer_null = Integer(choices=IntegerChoices, null=True)
    varchar = Varchar(choices=VarcharChoices)
    varchar_null = Varchar(choices=VarcharChoices, null=True)


###############################################################################
# Create the schema and populate data

TABLE_CLASSES: t.Tuple[t.Type[Table], ...] = (
    Director,
    Movie,
    Studio,
    User,
    Sessions,
    AuthenticatorSecret,
    Ticket,
    ArrayColumns,
    NullableColumns,
    RequiredColumns,
    SortedColumns,
    Constraints,
    ConstraintTarget,
    DateTimeColumns,
    Choices,
)


def set_engine(engine: str = "sqlite"):
    if engine == "postgres":
        db = PostgresEngine(config={"database": "piccolo_admin"})
    else:
        sqlite_path = os.path.join(os.path.dirname(__file__), "example.sqlite")
        db = SQLiteEngine(path=sqlite_path)  # type: ignore

    for table_class in TABLE_CLASSES:
        table_class._meta._db = db


def create_schema(persist: bool = False):
    if not persist:
        drop_db_tables_sync(*TABLE_CLASSES)

    create_db_tables_sync(*TABLE_CLASSES, if_not_exists=True)


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
    Studio.insert(*[Studio(**s) for s in STUDIOS]).run_sync()
    Ticket.insert(*[Ticket(**t) for t in TICKETS]).run_sync()
    SortedColumns.insert(
        *[SortedColumns(**s) for s in SORTED_COLUMNS]
    ).run_sync()

    if engine == "postgres":
        # We need to update the sequence, as we explicitly set the IDs for the
        # directors we just inserted
        Director.raw(
            "SELECT setval('director_id_seq', max(id)) FROM director"
        ).run_sync()

    # Create a user for testing login
    user = User(
        username=USERNAME,
        password=PASSWORD,
        email="admin@test.com",
        admin=True,
        active=True,
        superuser=True,
    )
    user.save().run_sync()

    new_user = User(
        username="john",
        password="john123",
        email="john@test.com",
        admin=True,
        active=True,
        superuser=False,
    )
    new_user.save().run_sync()

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

                directors = []
                genders = ["m", "f", "n"]
                for _ in range(chunk_size):
                    gender = random.choice(genders)
                    if gender == "m":
                        name = fake.name_male()
                    elif gender == "f":
                        name = fake.name_female()
                    else:
                        name = fake.name_nonbinary()
                    directors.append(Director(name=name, gender=gender))

                Director.insert(*directors).run_sync()

                director_ids = (
                    Director.select(Director._meta.primary_key)
                    .order_by(Director._meta.primary_key, ascending=False)
                    .limit(chunk_size)
                    .output(as_list=True)
                    .run_sync()
                )

                movies = []
                genres = [i.value for i in Movie.Genre]
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
                        release_date=fake.date(),
                        box_office=decimal.Decimal(
                            str(random.randint(10, 1500) / 10)
                        ),
                        barcode=random.randint(1_000_000_000, 9_999_999_999),
                        genre=random.choice(genres),
                    )
                    movies.append(movie)

                Movie.insert(*movies).run_sync()
