"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import asyncio
import datetime
import decimal
import enum
import logging
import os
import random
import smtplib
import typing as t

import targ
from hypercorn.asyncio import serve
from hypercorn.config import Config
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
from piccolo_api.media.local import LocalMediaStorage
from piccolo_api.media.s3 import S3MediaStorage
from piccolo_api.session_auth.tables import SessionsBase
from pydantic import BaseModel, field_validator
from starlette.requests import Request

from piccolo_admin.endpoints import (
    FormConfig,
    OrderBy,
    TableConfig,
    create_admin,
)
from piccolo_admin.example_data import (
    DIRECTORS,
    MOVIE_WORDS,
    MOVIES,
    SORTED_COLUMNS,
    STUDIOS,
    TICKETS,
)

logger = logging.getLogger()

try:
    """
    If you want to try out S3, create a .env file in this folder, with the
    following contents (inserting your S3 credentials where appropriate):

        AWS_ACCESS_KEY_ID=abc123
        AWS_SECRET_ACCESS_KEY=abc123
        BUCKET_NAME=bucket123

    These values can also be added if required:

        ENDPOINT_URL=s3.cloudprovider.com
        REGION_NAME=my-region

    The ``Director.photo`` column will then use S3 for storage.

    """

    import dotenv

    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    BUCKET_NAME = os.environ.get("BUCKET_NAME")

    USE_S3 = all(
        (
            AWS_SECRET_ACCESS_KEY,
            AWS_SECRET_ACCESS_KEY,
            BUCKET_NAME,
        )
    )

    if USE_S3:
        logger.info("Using S3")

        S3_CONFIG = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        }

        ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
        if ENDPOINT_URL:
            S3_CONFIG["endpoint_url"] = ENDPOINT_URL

        REGION_NAME = os.environ.get("REGION_NAME")
        if REGION_NAME:
            S3_CONFIG["region_name"] = REGION_NAME

except ImportError:
    USE_S3 = False


MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "example_media")
if not USE_S3 and not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)


USERNAME = "piccolo"
PASSWORD = "piccolo123"


class Sessions(SessionsBase):
    pass


class User(BaseUser, tablename="piccolo_user"):
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


###############################################################################


class BusinessEmailModel(BaseModel):
    email: str
    title: str = "Enquiry"
    content: str

    @field_validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("not valid email")
        return v


class BookingModel(BaseModel):
    email: str
    name: str
    notes: str = "N/A"

    @field_validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("not valid email")
        return v


def business_email_endpoint(request: Request, data: BusinessEmailModel) -> str:
    sender = "info@example.com"
    receivers = [data.email]

    message = f"""From: Piccolo Admin <info@example.com>
    To: Colleague <{data.email}>
    Subject: {data.title}
    {data.content}
    """

    try:
        smtpObj = smtplib.SMTP("localhost:1025")
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except (smtplib.SMTPException, ConnectionRefusedError):
        print("Error: unable to send email")

    return "Email sent"


def booking_endpoint(request: Request, data: BookingModel) -> str:
    """
    Testing that async functions works.
    """
    sender = "info@example.com"
    receivers = [data.email]

    message = f"""From: Bookings <info@example.com>
    To: To Friend <{data.email}>
    Subject: {data.name} booking
    {data.notes}
    """

    try:
        smtpObj = smtplib.SMTP("localhost:1025")
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except (smtplib.SMTPException, ConnectionRefusedError):
        print("Error: unable to send email")

    return "Booking complete"


TABLE_CLASSES: t.Tuple[t.Type[Table], ...] = (
    Director,
    Movie,
    Studio,
    User,
    Sessions,
    Ticket,
    NullableColumns,
    RequiredColumns,
    SortedColumns,
    Constraints,
    ConstraintTarget,
    DateTimeColumns,
)


movie_config = TableConfig(
    table_class=Movie,
    visible_columns=[
        Movie._meta.primary_key,
        Movie.name,
        Movie.rating,
        Movie.duration,
        Movie.director,
        Movie.won_oscar,
        Movie.poster,
        Movie.tags,
        Movie.screenshots,
    ],
    visible_filters=[
        Movie.name,
        Movie.rating,
        Movie.director,
        Movie.duration,
        Movie.genre,
        Movie.screenshots,
        Movie.poster,
        Movie.release_date,
    ],
    rich_text_columns=[Movie.description],
    media_storage=(
        LocalMediaStorage(
            column=Movie.poster,
            media_path=os.path.join(MEDIA_ROOT, "movie_poster"),
        ),
        LocalMediaStorage(
            column=Movie.screenshots,
            media_path=os.path.join(MEDIA_ROOT, "movie_screenshots"),
        ),
    ),
    menu_group="Movies",
    order_by=[OrderBy(Movie.rating, ascending=False)],
)

director_config = TableConfig(
    table_class=Director,
    visible_columns=[
        Director._meta.primary_key,
        Director.name,
        Director.gender,
        Director.photo,
    ],
    media_storage=(
        S3MediaStorage(
            column=Director.photo,
            bucket_name=t.cast(str, BUCKET_NAME),
            folder_name="director_photo",
            connection_kwargs=S3_CONFIG,
        )
        if USE_S3
        else LocalMediaStorage(
            column=Director.photo,
            media_path=os.path.join(MEDIA_ROOT, "photo"),
        ),
    ),
    menu_group="Movies",
)

studio_config = TableConfig(
    table_class=Studio,
    menu_group="Movies",
)

ticket_config = TableConfig(
    table_class=Ticket,
    menu_group="Booking",
    link_column=Ticket.booked_by,
    visible_columns=[
        Ticket.booked_by,
        Ticket.movie,
        Ticket.start_date,
        Ticket.start_time,
    ],
    time_resolution={Ticket.start_time: 60, Ticket.booked_on: 1},
)

nullable_config = TableConfig(
    table_class=NullableColumns,
    menu_group="Testing",
)

required_columns_config = TableConfig(
    table_class=RequiredColumns,
    menu_group="Testing",
)

sorted_columns_config = TableConfig(
    table_class=SortedColumns,
    order_by=[OrderBy(SortedColumns.integer, ascending=True)],
    menu_group="Testing",
)

constraints_config = TableConfig(
    table_class=Constraints,
    menu_group="Testing",
)

constraints_target_config = TableConfig(
    table_class=ConstraintTarget,
    menu_group="Testing",
)

date_time_config = TableConfig(
    table_class=DateTimeColumns, menu_group="Testing"
)

APP = create_admin(
    [
        movie_config,
        director_config,
        studio_config,
        ticket_config,
        nullable_config,
        required_columns_config,
        sorted_columns_config,
        constraints_config,
        constraints_target_config,
        date_time_config,
    ],
    forms=[
        FormConfig(
            name="Business email form",
            pydantic_model=BusinessEmailModel,
            endpoint=business_email_endpoint,
            description="Send an email to a business associate.",
        ),
        FormConfig(
            name="Booking form",
            pydantic_model=BookingModel,
            endpoint=booking_endpoint,
            description="Make a booking for a customer.",
        ),
    ],
    auth_table=User,
    session_table=Sessions,
    sidebar_links={
        "Top Movies": "/#/movie?__order=-box_office",
        "Google": "https://google.com",
    },
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


def main():
    cli = targ.CLI(description="Piccolo Admin")
    cli.register(run)
    cli.run(solo=True)


if __name__ == "__main__":
    main()
