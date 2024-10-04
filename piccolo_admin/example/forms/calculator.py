from pydantic import BaseModel
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


class CalculatorModel(BaseModel):
    number_1: int
    number_2: int


def calculator(request: Request, data: CalculatorModel):
    """
    A very simple example of a form which adds numbers together.
    """
    return f"The answer is {data.number_1 + data.number_2}."


FORM = FormConfig(
    name="Calculator",
    pydantic_model=CalculatorModel,
    endpoint=calculator,
    description=("Adds two numbers together."),
)
