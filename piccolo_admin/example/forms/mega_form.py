import datetime
import typing as t

from pydantic import BaseModel
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


class MegaFormModel(BaseModel):
    """
    Used for testing a wide variety of field types.
    """

    boolean_field: bool = True
    boolean_field_optional: t.Optional[bool] = None

    float_field: float = 1.0
    float_field_optional: t.Optional[float] = None

    integer_field: int = 1
    integer_field_optional: t.Optional[int] = None

    string_field: str = "Hello world"
    string_optional: t.Optional[str] = None

    list_field: t.List[str] = ["a", "b", "c"]
    list_field_optional: t.Optional[t.List[str]] = None

    time_field: datetime.time = datetime.time(hour=12, minute=30)
    time_field_optional: t.Optional[datetime.time] = None

    date_field: datetime.date = datetime.date(year=1999, month=12, day=31)
    date_field_optional: t.Optional[datetime.date] = None

    datetime_field: datetime.datetime = datetime.datetime(
        year=1999, month=12, day=31, hour=12, minute=30
    )
    datetime_field_optional: t.Optional[datetime.datetime] = None

    timedelta_field: datetime.timedelta = datetime.timedelta(hours=1)
    timedelta_field_optional: t.Optional[datetime.timedelta] = None


async def handle_form(request: Request, data: MegaFormModel) -> str:
    return data.model_dump_json(indent=4)


FORM = FormConfig(
    name="Mega Form",
    pydantic_model=MegaFormModel,
    endpoint=handle_form,
    description="Used for testing all possible field types.",
    form_group="Test forms",
)
