import datetime

from playwright.sync_api import Page

from piccolo_admin.example.tables import DateTimeColumns

from .pages import AddRowPage, LoginPage


def test_date_time_columns(page: Page, dev_server):
    """
    Make sure we can submit a form containing `Date` / `Time` / `Timestamp` /
    `Timestamptz` columns, and it gets saved in the database.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = AddRowPage(
        page=page, tablename=DateTimeColumns._meta.tablename
    )
    test_page.reset()

    # Let Vue JS finish loading before submitting
    page.wait_for_timeout(1000)
    test_page.submit_form()

    response = DateTimeColumns.select().run_sync()
    row = response[0]

    for column_name in (
        "date_null",
        "time_null",
        "timestamp_null",
        "timestamptz_null",
    ):
        assert row[column_name] is None

    for column_name in ("timestamp", "timestamptz"):
        assert isinstance(row[column_name], datetime.datetime)

    assert isinstance(row["date"], datetime.date)
    assert isinstance(row["time"], datetime.time)
