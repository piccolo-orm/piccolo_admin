from playwright.sync_api import Page

from piccolo_admin.example.tables import NullableColumns

from .pages import AddRowPage, LoginPage, RowListingPage


def test_add_nullable_columns(page: Page, dev_server):
    """
    Make sure we can submit a form containing nullable columns, and it gets
    saved in the database.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = AddRowPage(
        page=page, tablename=NullableColumns._meta.tablename
    )
    test_page.reset()
    test_page.submit_form()

    response = NullableColumns.select().run_sync()
    assert response == [
        {
            "id": 1,
            "integer": None,
            "real": None,
            "numeric": None,
            "uuid": None,
            "email": None,
            "timestamp": None,
            "date": None,
            "json_": None,
            "varchar": None,
            "text": None,
            "boolean": None,
        }
    ]


def test_nullable_boolean_filter(page: Page, dev_server):
    """
    Make sure that nullable boolean columns in the filter sidebar default to
    `all` and NOT `null`.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    row_listing_page = RowListingPage(
        page=page, tablename=NullableColumns._meta.tablename
    )
    row_listing_page.reset()
    row_listing_page.open_filter_sidebar()

    html_select = row_listing_page.filter_sidebar.get_input("boolean")
    assert html_select.input_value() == "all"
