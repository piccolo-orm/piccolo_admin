from fastapi import FastAPI
from fastapi.routing import Mount
from home.tables import Director, Movie
from piccolo.query.methods.select import Count

from piccolo_admin.endpoints import ChartConfig, create_admin


async def get_director_movie_count():
    """
    Returns the number of movies per director.
    """
    movies = await Movie.select(
        Movie.director.name.as_alias("director"),
        Count(Movie.id),
    ).group_by(Movie.director)

    # Flatten the response so it's a list of lists
    # like [['George Lucas', 3], ...]
    return [(i["director"], i["count"]) for i in movies]


director_chart = ChartConfig(
    title="Movie count",
    chart_type="Pie",
    data_source=get_director_movie_count,
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

# For Starlette it is identical, just use `app = Starlette(...)`
