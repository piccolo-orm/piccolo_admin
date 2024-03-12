from playwright.sync_api import Page

from piccolo_admin.example import ArrayColumns

from .pages import AddRowPage, LoginPage


def test_add_array_columns(page: Page, dev_server):
    """
    Make sure we can submit a form containing array columns, and it gets
    saved in the database.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = AddRowPage(page=page, tablename=ArrayColumns._meta.tablename)
    test_page.reset()

    # Let Vue JS finish loading
    page.wait_for_timeout(1000)

    test_page.add_array_value(
        field="varchar",
        value="Alice",
    )

    test_page.add_array_value(
        field="integer",
        value="1",
    )

    test_page.add_array_value(
        field="email",
        value="test@gmail.com",
    )

    test_page.submit_form()

    response = ArrayColumns.select(
        ArrayColumns.varchar,
        ArrayColumns.integer,
        ArrayColumns.email,
    ).run_sync()

    assert {
        "varchar": ["Alice"],
        "integer": [1],
        "email": ["test@gmail.com"],
    } in response


def _test_value(page: Page, field: str, value: str):
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = AddRowPage(page=page, tablename=ArrayColumns._meta.tablename)
    test_page.reset()

    # Let Vue JS finish loading
    page.wait_for_timeout(1000)

    test_page.add_array_value(
        field="email",
        value="hello world",
    )

    test_page.submit_form(expected_status=422)

    assert test_page.error_list.get_error_count() > 0


def test_array_varchar_validation(page: Page, dev_server):
    """
    Make sure that text values which are too long are rejected.
    """
    _test_value(
        page=page,
        field="email",
        value="a"
        * (ArrayColumns.varchar.base_column._meta.params["length"] + 1),
    )


def test_array_email_validation(page: Page, dev_server):
    """
    Make sure that invalid email values are rejected.
    """
    _test_value(page=page, field="email", value="hello world")


def test_array_integer_validation(page: Page, dev_server):
    """
    Make sure that invalid integer values are rejected.
    """
    _test_value(page=page, field="integer", value="a")
