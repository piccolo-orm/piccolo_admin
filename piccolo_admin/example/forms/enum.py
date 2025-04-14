import enum

from pydantic import BaseModel, EmailStr
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


# An example of using Python enum in custom forms
class Permission(str, enum.Enum):
    admissions = "admissions"
    gallery = "gallery"
    notices = "notices"
    uploads = "uploads"


class NewStaffModel(BaseModel):
    username: str
    email: EmailStr
    superuser: bool


def new_staff_endpoint(request: Request, data: NewStaffModel) -> str:
    print(data)
    return "A new staff member has been successfully created."


FORM = FormConfig(
    name="Enum form",
    pydantic_model=NewStaffModel,
    endpoint=new_staff_endpoint,
    description="Make a enum form.",
    choices={"permissions": Permission},
    form_group="Text forms",
)
