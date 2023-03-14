"""
By using pages we can make out test more scalable.

https://playwright.dev/docs/pom
"""

from playwright.sync_api import Page

from .conftest import BASE_URL, PASSWORD, USERNAME


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
        self.login_button.click()


class NullableColumnsTableAdd:
    url = f"{BASE_URL}/#/nullable_columns/add"

    def __init__(self, page: Page):
        self.page = page
        self.create_button = page.locator("button[data-uitest=create_button]")

    def reset(self):
        self.page.goto(self.url)

    def submit_form(self):
        self.create_button.click()
