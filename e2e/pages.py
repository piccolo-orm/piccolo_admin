"""
By using pages we can make out test more scalable.

https://playwright.dev/docs/pom
"""

from playwright.sync_api import Page

from piccolo_admin.example import PASSWORD, USERNAME

from .conftest import BASE_URL


class LoginPage:
    url = f"{BASE_URL}/#/login"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('input[name="username"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('button[data-uitest="login_button"]')

    def reset(self):
        self.page.goto(self.url)

    def login(self):
        self.username_input.fill(USERNAME)
        self.password_input.fill(PASSWORD)

        with self.page.expect_response(
            lambda response: response.url == f"{BASE_URL}/public/login/"
            and response.request.method == "POST"
            and response.status == 200
        ):
            self.login_button.click()


class RowListingPage:
    def __init__(self, page: Page, tablename: str):
        self.page = page
        self.url = f"{BASE_URL}/#/{tablename}"
        self.sort_button = page.locator("a[data-uitest=sort_button]")
        self.sort_by_selector = page.locator(
            "select[data-uitest=sort_by_selector]"
        )

    def reset(self):
        self.page.goto(self.url)

    def open_sort_modal(self):
        self.sort_button.click()

    def get_sort_by_column(self) -> str:
        """
        Returns the name of the column being sorted by.
        """
        return self.sort_by_selector.input_value()


class AddRowPage:
    def __init__(self, page: Page, tablename: str):
        self.page = page
        self.tablename = tablename
        self.url = f"{BASE_URL}/#/{tablename}/add"
        self.create_button = page.locator("button[data-uitest=create_button]")

    def reset(self):
        self.page.goto(self.url)

    def submit_form(self):
        with self.page.expect_response(
            lambda response: response.url
            == f"{BASE_URL}/api/tables/{self.tablename}/"
            and response.request.method == "POST"
            and response.status == 201
        ):
            self.create_button.click()
