from fastapi import FastAPI
from fastapi.routing import Mount
from pydantic import BaseModel
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig, create_admin


# Pydantic model for the form
class CalculatorModel(BaseModel):
    number_1: int
    number_2: int


# Endpoint for handling the form
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
    form_group="Text forms",
)


app = FastAPI(
    routes=[
        Mount(
            "/admin/",
            create_admin(forms=[FORM]),
        ),
    ],
)

# For Starlette it is identical, just `app = Starlette(...)`
