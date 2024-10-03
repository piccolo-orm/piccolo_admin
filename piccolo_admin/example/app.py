"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example.app`,
or `admin_demo`.
"""

import asyncio
import logging
import os
import typing as t

import targ
from hypercorn.asyncio import serve
from hypercorn.config import Config
from piccolo_api.encryption.providers import XChaCha20Provider
from piccolo_api.media.local import LocalMediaStorage
from piccolo_api.media.s3 import S3MediaStorage
from piccolo_api.mfa.authenticator.provider import AuthenticatorProvider

from piccolo_admin.endpoints import OrderBy, TableConfig, create_admin
from piccolo_admin.example.forms import FORMS
from piccolo_admin.example.tables import (
    ArrayColumns,
    AuthenticatorSecret,
    Choices,
    Constraints,
    ConstraintTarget,
    DateTimeColumns,
    Director,
    Movie,
    NullableColumns,
    RequiredColumns,
    Sessions,
    SortedColumns,
    Studio,
    Ticket,
    User,
    create_schema,
    populate_data,
    set_engine,
)

logger = logging.getLogger()


###############################################################################
# Setup S3 integration if required

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


###############################################################################
# Configure tables

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
        (
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
            )
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

array_columns_config = TableConfig(
    table_class=ArrayColumns, menu_group="Testing"
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

choices_config = TableConfig(
    table_class=Choices,
    menu_group="Testing",
)

###############################################################################

APP = create_admin(
    [
        movie_config,
        director_config,
        studio_config,
        ticket_config,
        array_columns_config,
        nullable_config,
        required_columns_config,
        sorted_columns_config,
        constraints_config,
        constraints_target_config,
        date_time_config,
        choices_config,
    ],
    forms=FORMS,
    auth_table=User,
    session_table=Sessions,
    sidebar_links={
        "Top Movies": "/#/movie?__order=-box_office",
        "Google": "https://google.com",
    },
    mfa_providers=[
        AuthenticatorProvider(
            encryption_provider=XChaCha20Provider(
                encryption_key=(
                    b"\x01\xfdN\xe4E?\xaa\xf8<e\xfc\x9f\x0b9\x8b\x00H%~\xe1/\xd7\xdcz\xff\xd88\xdajd\xae\x06"  # noqa: E501
                )
            ),
            secret_table=AuthenticatorSecret,
        ),
    ],
)


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
