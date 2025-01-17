from enum import Enum

from pydantic import BaseModel
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


class Options(Enum):
    ONE = "One"
    TWO = "Two"
    THREE = "Three"


class SelectionModel(BaseModel):
    option: Options = Options.ONE


def selection(request: Request, data: SelectionModel):
    """
    A very simple example of a form which provides a selection drop down.
    """
    return (
        f"You selected {data.option} from the drop down."
    )


FORM = FormConfig(
    name="Selection",
    pydantic_model=SelectionModel,
    endpoint=selection,
    description="Provides an example usage of drop downs within custom forms.",
)
