"""
Runs the admin in read only mode - useful for letting people evaluate the admin
online without risk of abuse.
"""

import targ
import uvicorn

from piccolo_admin.endpoints import create_admin
from piccolo_admin.example.forms.calculator import FORM as CALCULATOR_FORM
from piccolo_admin.example.forms.csv import FORM as CSV_FORM
from piccolo_admin.example.forms.email import FORM as BOOKING_FORM
from piccolo_admin.example.forms.image import FORM as IMAGE_FORM
from piccolo_admin.example.tables import (
    Director,
    Movie,
    Sessions,
    User,
    create_schema,
    populate_data,
    set_engine,
)

APP = create_admin(
    [Director, Movie],
    auth_table=User,
    session_table=Sessions,
    read_only=True,
    forms=[
        BOOKING_FORM,
        CALCULATOR_FORM,
        CSV_FORM,
        IMAGE_FORM,
    ],
)


def sandbox(host: str = "localhost", port: int = 8080):
    """
    Run the Piccolo Admin in read only mode with a SQLite database.

    :param host:
        Which host to serve the app on.
    :param host:
        Which port to serve the app on.

    """
    set_engine()
    create_schema(persist=False)
    populate_data()

    uvicorn.run(APP, host=host, port=port)


if __name__ == "__main__":
    cli = targ.CLI()
    cli.register(sandbox)
    cli.run(solo=True)
