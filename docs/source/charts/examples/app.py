import asyncio

from fastapi import FastAPI
from fastapi.routing import Mount
from home.tables import Director, Movie

from piccolo_admin.endpoints import ChartConfig, create_admin


# count directors movies
async def director_movie_count():
    movies = await Movie.select(
        Movie.director.name.as_alias("director"),
        Count(Movie.id),
    ).group_by(Movie.director)
    # Flatten the response so it's a list of lists
    # like [['George Lucas', 3], ...]
    return [[i["director"], i["count"]] for i in movies]


chart_data = asyncio.run(director_movie_count())


director_chart = ChartConfig(
    title="Movie count",
    chart_type="Pie",
    data=chart_data,
)


app = FastAPI(
    routes=[
        Mount(
            "/admin/",
            create_admin(
                tables=[Director, Movie],
                charts=[director_chart],
            ),
        ),
    ],
)

# For Starlette it is identical, just `app = Starlette(...)`
