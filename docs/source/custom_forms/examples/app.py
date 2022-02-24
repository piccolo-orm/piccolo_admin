import smtplib

from fastapi import FastAPI
from fastapi.routing import Mount
from home.tables import Task
from pydantic import BaseModel

from piccolo_admin.endpoints import FormConfig, create_admin


# Pydantic model for form
class EmailFormModel(BaseModel):
    email: str
    title: str
    content: str


# Send email handler
def email_endpoint(request, data):
    sender = "info@example.com"
    receivers = data.email

    message = f"""From: Sender <info@example.com>
    To: Receiver <{data.email}>
    Subject: {data.title}
    {data.content}
    """

    try:
        smtpObj = smtplib.SMTP("localhost:1025")
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")

    return "Email sent"


app = FastAPI(
    routes=[
        Mount(
            "/admin/",
            create_admin(
                tables=[Task],
                forms=[
                    FormConfig(
                        name="Business Email Form",
                        pydantic_model=EmailFormModel,
                        endpoint=email_endpoint,
                    ),
                ],
            ),
        ),
    ],
)

# For Starlette it is identical, just `app = Starlette(...)`
