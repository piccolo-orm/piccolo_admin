"""
An example of how to configure and run the admin.

Can be run from the command line using python example.py
"""
import os

import uvicorn
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.extensions.user import BaseUser
from piccolo.table import Table
from piccolo.columns import Varchar, Integer

from endpoints import AdminRouter


DB_PATH = 'example.sqlite'
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
    path = os.path.join(os.path.dirname(__file__), DB_PATH)
    if os.path.exists(path):
        os.unlink(path)
    Movie.create.run_sync()
    User.create.run_sync()

    # Run the admin
    app = AdminRouter(Movie, auth_table=User)
    uvicorn.run(app)


if __name__ == "__main__":
    main()
