import datetime

from playwright.sync_api import Page

from piccolo_admin.example import Choices

from .pages import AddRowPage, LoginPage


def test_choices(page: Page, dev_server):
    """
    Make sure choices work as expected.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    add_row_page = AddRowPage(
        page=page,
        tablename=Choices._meta.tablename,
    )
    add_row_page.reset()

    # Let Vue JS finish loading
    page.wait_for_timeout(1000)

    for field in ("array", "array_null"):
        add_row_page.add_array_item(field=field, option="a")

    for field in ("date", "date_null"):
        add_row_page.select_value(field=field, option="2000-01-01")

    for field in ("integer", "integer_null"):
        add_row_page.select_value(field=field, option="1")

    for field in ("varchar", "varchar_null"):
        add_row_page.select_value(field=field, option="a")

    add_row_page.submit_form()

    choices_in_db = Choices.select(
        Choices.all_columns(exclude=[Choices.id])
    ).run_sync()

    assert {
        "array": ["a"],
        "array_null": ["a"],
        "date": datetime.date(2000, 1, 1),
        "date_null": datetime.date(2000, 1, 1),
        "integer": 1,
        "integer_null": 1,
        "varchar": "a",
        "varchar_null": "a",
    } in choices_in_db
