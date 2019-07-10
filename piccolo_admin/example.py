"""
An example of how to configure and run the admin.

Can be run from the command line using `python -m piccolo_admin.example`,
or `admin_demo`.
"""
import os

import uvicorn
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.extensions.user import BaseUser
from piccolo.table import Table
from piccolo.columns import Varchar, Integer

from piccolo_admin.endpoints import create_admin


DB_PATH = os.path.join(os.path.dirname(__file__), 'example.sqlite')
DB = SQLiteEngine(path=DB_PATH)


class User(BaseUser):
    class Meta():
        db = DB


class Movie(Table):
    name = Varchar(length=300)
    rating = Integer()

    class Meta():
        db = DB


def main():
    # Recreate the database
    if os.path.exists(DB_PATH):
        os.unlink(DB_PATH)
    Movie.create.run_sync()
    User.create.run_sync()

    # Run the admin
    app = create_admin([Movie], auth_table=User)
    uvicorn.run(app)


if __name__ == "__main__":
    main()
