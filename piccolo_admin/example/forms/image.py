import datetime
import io
import os
import shutil

from pydantic import BaseModel
from starlette.requests import Request

from piccolo_admin.endpoints import FileResponse, FormConfig


class DownloadScheduleModel(BaseModel):
    date: datetime.date


def download_schedule(
    request: Request, data: DownloadScheduleModel
) -> FileResponse:
    """
    An example form function which downloads an image file.
    """
    file_name = "movie_listings.jpg"
    with open(
        os.path.join(os.path.dirname(__file__), "files", file_name),
        "rb",
    ) as f:
        output_file = io.BytesIO()
        shutil.copyfileobj(f, output_file)

    return FileResponse(
        contents=output_file,
        file_name=file_name,
        media_type="image/jpeg",
    )


FORM = FormConfig(
    name="Download schedule",
    pydantic_model=DownloadScheduleModel,
    endpoint=download_schedule,
    description=("Download the schedule for the day."),
)
