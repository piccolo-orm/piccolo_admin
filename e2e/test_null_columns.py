from playwright.sync_api import Page

from piccolo_admin.example import NullableColumns

from .pages import AddRowPage, LoginPage


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
        }
    ]
