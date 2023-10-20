from playwright.sync_api import Page

from piccolo_admin.example import Director

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

    name_input = page.locator('input[name="name"]')
    name_input.fill("Steven Spielberg")

    gender_select = page.locator('select[name="gender"]')
    gender_select.select_option("m")

    add_row_page.submit_form()

    assert (
        Director.exists().where(Director.name == "Steven Spielberg").run_sync()
    )
