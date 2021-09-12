.. _CustomForms:

Custom Forms
============

Piccolo Admin has ability to turn a Pydantic model into a form in the UI, 
and we can use it for automatic creation of custom forms in Piccolo Admin 
without writing frontend code.

Example of creating and sending email form in FastAPI:

.. code-block:: python

    import smtplib
    from fastapi import FastAPI
    from piccolo_admin.endpoints import (
        create_admin,
        FormConfig,
    )
    from pydantic import BaseModel
    from home.tables import Task

    # Pydantic model for form 
    class EmailFormModel(BaseModel):
        email: str
        title: str
        content: str

    # Send email handler
    def email_endpoint(request, data):
        sender = "info@example.com"
        receivers = [data["email"]]

        message = f"""From: From sender <info@example.com>
        To: To reciever <{data["email"]}>
        Subject: {data["title"]}
        {data["content"]}
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
                            name="Email form",
                            pydantic_model=EmailFormModel,
                            endpoint=email_endpoint,
                        ),
                    ],
                ),
            ),
        ],
    )


Piccolo Admin will then show a custom form in UI. To process the form, 
you only need to specify the Pydantic model and function which processing 
your custom form and Piccolo Admin will do the rest like in above example.


