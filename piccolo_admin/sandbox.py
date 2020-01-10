"""
Runs the admin in read only mode - useful for letting people evaluate the admin
online without risk of abuse.
"""
import sys

import uvicorn
from piccolo_admin.example import (
    Director,
    Movie,
    Sessions,
    User,
    create_admin,
    populate_data,
)


APP = create_admin(
    [Director, Movie], auth_table=User, session_table=Sessions, read_only=True
)


def main(host="localhost", port=8080):
    populate_data()
    uvicorn.run(APP, host=host, port=port)


if __name__ == "__main__":
    args = sys.argv
    kwargs = {}
    if "--production" in args:
        kwargs.update({"host": "0.0.0.0", "port": 80})

    main(**kwargs)
