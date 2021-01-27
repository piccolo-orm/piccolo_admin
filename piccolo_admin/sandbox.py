"""
Runs the admin in read only mode - useful for letting people evaluate the admin
online without risk of abuse.
"""
from piccolo_admin.example import (
    Director,
    Movie,
    Sessions,
    User,
    create_admin,
    create_schema,
    populate_data,
    set_engine,
)
import targ
import uvicorn


APP = create_admin(
    [Director, Movie], auth_table=User, session_table=Sessions, read_only=True
)


def run(host="localhost", port=8080):
    set_engine()
    create_schema(persist=False)
    populate_data()
    uvicorn.run(APP, host=host, port=port)


def sandbox(production: bool = False):
    """
    Run the Piccolo Admin in read only mode with a SQLite database.
    """
    kwargs = {}
    if production:
        kwargs.update({"host": "0.0.0.0", "port": 80})

    run(**kwargs)


if __name__ == "__main__":
    cli = targ.CLI()
    cli.register(sandbox)
    cli.run(solo=True)
