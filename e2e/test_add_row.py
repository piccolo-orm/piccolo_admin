from playwright.sync_api import Page

from piccolo_admin.example.tables import Director

from .pages import AddRowPage, LoginPage


def test_add_row(page: Page, dev_server):
    """
    Make sure rows can be added.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    add_row_page = AddRowPage(
        page=page,
        tablename=Director._meta.tablename,
    )
    add_row_page.reset()

    # Let Vue JS finish loading
    page.wait_for_timeout(1000)

    test_name = "Steven Spielberg"
    name_input = page.locator('input[name="name"]')
    name_input.click()
    name_input.fill(test_name)

    gender_select = page.locator('select[name="gender"]')
    gender_select.select_option("m")

    add_row_page.submit_form()

    assert Director.exists().where(Director.name == test_name).run_sync()
