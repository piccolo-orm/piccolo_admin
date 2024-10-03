from playwright.sync_api import Page

from piccolo_admin.example.app import OrderBy
from piccolo_admin.example.tables import SortedColumns

from .conftest import BASE_URL
from .pages import LoginPage, RowListingPage


def test_sort_columns(page: Page, dev_server):
    """
    Make sure that custom sort works on the row listing page. The column name
    should match what we specified in ``TableConfig``.
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

    # Add a second sort column
    test_page.sort_modal.click_add_sort_column_button()
    assert test_page.sort_modal.get_column_count() == 2

    # Remove it again to make sure that works
    test_page.sort_modal.click_remove_column_button()
    assert test_page.sort_modal.get_column_count() == 1

    # Add a second sort column again
    test_page.sort_modal.click_add_sort_column_button()
    assert test_page.sort_modal.get_column_count() == 2

    # Specify the sort we want, and submit the form.
    # Make sure the API call was made.
    test_page.sort_modal.populate_form(
        order_by_list=[
            OrderBy(column=SortedColumns.integer),
            OrderBy(column=SortedColumns.letter),
        ]
    )
    with page.expect_response(
        lambda response: response.url
        == f"{BASE_URL}/api/tables/sorted_columns/?__readable=true&__order=integer,letter&__page_size=15&__page=1"  # noqa: E501
        and response.request.method == "GET"
        and response.status == 200
    ):
        test_page.sort_modal.submit_form()

    # We store the order in the URL, so people can share the URL or reload it
    # and get the same results.
    assert "?__order=integer,letter" in page.url
