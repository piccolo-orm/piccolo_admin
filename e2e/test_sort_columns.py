from playwright.sync_api import Page

from piccolo_admin.example import SortedColumns

from .pages import LoginPage, RowListingPage


def test_sort_columns(page: Page, dev_server):
    """
    Make sure that custom sort works on the row listing page.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = RowListingPage(
        page=page, tablename=SortedColumns._meta.tablename
    )
    test_page.reset()
    test_page.open_sort_modal()

    assert (
        test_page.sort_modal.get_sort_by_column()
        == SortedColumns.integer._meta.name
    )


def test_add_sort_column(page: Page, dev_server):
    """
    Make sure we can add and remove columns in the sort modal.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = RowListingPage(
        page=page, tablename=SortedColumns._meta.tablename
    )
    test_page.reset()
    test_page.open_sort_modal()
    test_page.sort_modal.click_add_sort_column_button()
    assert test_page.sort_modal.get_column_count() == 2
