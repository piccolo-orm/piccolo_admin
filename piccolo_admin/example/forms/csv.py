import csv
import io

from pydantic import BaseModel, field_validator
from starlette.requests import Request

from piccolo_admin.endpoints import FileResponse, FormConfig
from piccolo_admin.example.tables import Movie


class DownloadMoviesModel(BaseModel):
    director_name: str

    @field_validator("director_name")
    def validate_director_name(cls, v):
        if v == "":
            raise ValueError("The value can't be empty.")
        return v


async def download_movies(
    request: Request, data: DownloadMoviesModel
) -> FileResponse:
    """
    An example custom form function which downloads a CSV file.
    """
    movies = await Movie.select(Movie.name, Movie.release_date).where(
        Movie.director._.name == data.director_name
    )

    output_file = io.StringIO(None)

    writer = csv.DictWriter(
        f=output_file,
        fieldnames=["name", "release_date"],
    )
    writer.writeheader()
    writer.writerows(movies)

    return FileResponse(
        contents=output_file,
        file_name="director_movies.csv",
        media_type="text/csv",
    )


FORM = FormConfig(
    name="Download director movies",
    pydantic_model=DownloadMoviesModel,
    endpoint=download_movies,
    description="Download a list of movies for the director as a CSV file.",
)
