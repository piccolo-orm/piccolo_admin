from playwright.sync_api import Page

from .pages import HomePage, LoginPage


def test_logout(page: Page, dev_server):
    """
    Make sure the user can logout.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    home_page = HomePage(page=page)
    home_page.nav.logout()
