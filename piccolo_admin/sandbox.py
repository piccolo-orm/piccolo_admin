"""
Runs the admin in read only mode - useful for letting people evaluate the admin
online without risk of abuse.
"""
import targ
import uvicorn
from piccolo.apps.user.tables import BaseUser
from piccolo_api.session_auth.tables import SessionsBase

from piccolo_admin.example import (
    Director,
    Movie,
    create_admin,
    create_schema,
    populate_data,
    set_engine,
)

APP = create_admin(
    [Director, Movie],
    auth_table=BaseUser,
    session_table=SessionsBase,
    read_only=True,
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
