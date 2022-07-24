# app.py
from fastapi import FastAPI
from fastapi.routing import Mount
from movies.tables import Director, Movie
from piccolo.engine import engine_finder

from piccolo_admin.endpoints import create_admin

app = FastAPI(
    routes=[
        Mount(
            path="/admin/",
            app=create_admin(
                tables=[Director, Movie],
                # Specify a different site name in the
                # admin UI (default Piccolo Admin):
                site_name="My Site Admin",
                # Required when running under HTTPS:
                # allowed_hosts=["my_site.com"],
            ),
        ),
    ],
)


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connnection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connnection_pool()
