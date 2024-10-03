import datetime
import smtplib

from pydantic import BaseModel, EmailStr
from starlette.requests import Request

from piccolo_admin.endpoints import FormConfig


class BookingModel(BaseModel):
    movie: str = "Star Wars: Episode IV - A New Hope"
    email: EmailStr
    name: str
    tickets: int
    starts_at: datetime.datetime
    notes: str = "N/A"


def booking_endpoint(request: Request, data: BookingModel) -> str:
    """
    An example form function which sends an email.
    """
    sender = "info@example.com"
    receivers = [data.email]

    message = f"""From: Bookings <info@example.com>
    To: Customer <{data.email}>
    Subject: {data.name} booked {data.tickets} ticket(s) for {data.starts_at}.
    {data.notes}
    """

    try:
        smtpObj = smtplib.SMTP("localhost:1025")
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except (smtplib.SMTPException, ConnectionRefusedError):
        print("Error: unable to send email")

    return "Booking complete"


FORM = FormConfig(
    name="Booking form",
    pydantic_model=BookingModel,
    endpoint=booking_endpoint,
    description="Make a booking for a customer.",
)
