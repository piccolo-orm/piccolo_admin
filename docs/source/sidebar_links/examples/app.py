# app.py
from fastapi import FastAPI
from fastapi.routing import Mount
from piccolo_admin.endpoints import create_admin

from movies.tables import Director, Movie


app = FastAPI(
    routes=[
        Mount(
            path="/admin/",
            app=create_admin(
                tables=[Director, Movie],
                sidebar_links={
                    "Top Movies": "/admin/#/movie?__order=-box_office",
                    "Google": "https://google.com"
                },
            ),
        ),
    ],
)
