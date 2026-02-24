import enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


# An example of using Python enum in custom forms
class Permission(str, enum.Enum):
    admissions = "admissions"
    gallery = "gallery"
    notices = "notices"
    uploads = "uploads"

class LogLevel(int, enum.Enum):
    error = 2
    warn = 3
    info = 4
    debug = 5

class NewStaffModel(BaseModel):
    username: str
    email: EmailStr
    superuser: bool
    permissions: Permission="gallery"
    log_level: Optional[LogLevel]


def new_staff_endpoint(request: Request, data: NewStaffModel) -> str:
    # We need to do the enum type conversion ourselves like this:
    # data.permissions = Permission(int(data.permissions)) # for int enum
    # data.permissions = Permission(data.permissions)  # for str enum
    print(data)
    return "A new staff member has been successfully created."


FORM = FormConfig(
    name="Enum form",
    pydantic_model=NewStaffModel,
    endpoint=new_staff_endpoint,
    description="Make a enum form.",
    form_group="Text forms",
)
