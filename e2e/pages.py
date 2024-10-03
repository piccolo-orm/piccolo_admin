"""
By using pages we can make out test more scalable.

https://playwright.dev/docs/pom
"""

import typing as t

from playwright.sync_api import Page

from piccolo_admin.example.app import OrderBy
from piccolo_admin.example.tables import PASSWORD, USERNAME

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

        self.page.wait_for_url(f"{BASE_URL}/#/")


###############################################################################
# Row listing page


class SortModal:
    """
    Part of :class:`RowListingPage`.
    """

    def __init__(self, page: Page):
        self.sort_by_selector = page.locator(
            "select[data-uitest=sort_by_selector]"
        )
        self.add_sort_column_button = page.locator(
            "a[data-uitest=add_sort_column_button]"
        )
        self.column_selects = page.locator("select[name=column]")
        self.remove_column_buttons = page.locator(
            "a[data-uitest=remove_column_button]"
        )
        self.submit_button = page.locator(
            "button[data-uitest=sort_form_button]"
        )

    def click_add_sort_column_button(self):
        self.add_sort_column_button.click()

    def click_remove_column_button(self):
        """
        As there are potentially multiple remove column buttons, we click the
        bottom one.
        """
        self.remove_column_buttons.last.click()

    def submit_form(self):
        self.submit_button.click()

    def get_sort_by_column(self) -> str:
        """
        Returns the name of the column being sorted by.
        """
        return self.sort_by_selector.input_value()

    def get_column_count(self) -> int:
        """
        Returns the number of columns being sorted by in the UI.
        """
        return self.column_selects.count()

    def populate_form(self, order_by_list: t.List[OrderBy]):
        """
        Make sure we have enough column select elements, and populate them.
        """
        if len(order_by_list) == 0:
            return

        column_selects = self.column_selects

        existing_count = column_selects.count()

        delta = len(order_by_list) - existing_count
        if delta > 0:
            for _ in range(delta):
                self.click_remove_column_button()
        else:
            for _ in range(delta * -1):
                self.click_add_sort_column_button()

        for index, order_by in enumerate(order_by_list):
            column_select = self.column_selects.nth(index)
            column_select.select_option(order_by.column._meta.name)


class FilterSidebar:
    """
    Part of :class:`RowListingPage`.
    """

    def __init__(self, page: Page):
        self.sidebar = page.locator("div[data-uitest=right_sidebar]")
        self.submit_button = self.sidebar.locator(
            "button[data-uitest=submit_filter_button]"
        )

    def get_input(self, name: str):
        """
        Returns the value of an input or select in the sidebar.

        :param name:
            The name of the input or select.

        """
        return self.sidebar.locator(f"[name={name}]")

    def get_operator_selector(self, name: str):
        """
        Returns the operator selector.

        :param name:
            The name of the field.

        """
        return self.sidebar.locator(f"[name={name}__operator]")

    def get_match_selector(self, name: str):
        """
        Returns the match selector.

        :param name:
            The name of the field.

        """
        return self.sidebar.locator(f"[name={name}__match]")

    def submit_form(self):
        """
        Submits the filter form.
        """
        self.submit_button.click()


class CSVModal:
    """
    Part of :class:`RowListingPage`.
    """

    def __init__(self, page: Page):
        self.modal = page.locator("div[data-uitest=csv_modal]")
        self.download_button = self.modal.locator(
            "button[data-uitest=download_csv_button]"
        )

    def click_download(self):
        self.download_button.click()


class RowListingPage:
    def __init__(self, page: Page, tablename: str):
        self.page = page
        self.url = f"{BASE_URL}/#/{tablename}"
        self.sort_button = page.locator("a[data-uitest=sort_button]")
        self.filter_button = page.locator("a[data-uitest=filter_button]")
        self.csv_button = page.locator("a[data-uitest=csv_button]")
        self.csv_modal = CSVModal(page=page)
        self.filter_sidebar = FilterSidebar(page=page)
        self.sort_modal = SortModal(page=page)

    def reset(self):
        self.page.goto(self.url)

    def open_sort_modal(self):
        self.sort_button.click()

    def open_filter_sidebar(self):
        self.filter_button.click()

    def show_csv_modal(self):
        self.csv_button.click()


###############################################################################


class ErrorList:
    def __init__(self, page: Page):
        self.page = page
        self.error_div = page.locator("div.errors")

    def check_error(self, error: str):
        list_item = self.error_div.locator("li:first-child")
        assert error == list_item.inner_text()

    def get_error_count(self) -> int:
        return self.error_div.locator("li").count()


class EditRowPage:
    def __init__(self, page: Page, tablename: str, row_id: str):
        self.page = page
        self.tablename = tablename
        self.row_id = row_id
        self.url = f"{BASE_URL}/#/{tablename}/{row_id}/"
        self.drop_down_button = page.locator("a[data-uitest=drop_down_button]")
        self.delete_row_button = page.locator(
            "a[data-uitest=delete_row_button]"
        )
        self.error_list = ErrorList(page=page)
        self.save_button = page.locator("button[data-uitest=save_button]")

    def open_drop_down_menu(self):
        self.drop_down_button.click()

    def delete(self):
        self.open_drop_down_menu()
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.delete_row_button.click()

    def save(self):
        with self.page.expect_response(
            lambda response: response.url
            == f"{BASE_URL}/api/tables/{self.tablename}/{self.row_id}/"
            and response.request.method == "PATCH"
            and response.status == 200
        ):
            self.save_button.click()

    def reset(self):
        self.page.goto(self.url)


###############################################################################


class AddRowPage:
    def __init__(self, page: Page, tablename: str):
        self.page = page
        self.tablename = tablename
        self.url = f"{BASE_URL}/#/{tablename}/add"
        self.error_list = ErrorList(page=page)
        self.create_button = page.locator("button[data-uitest=create_button]")

    def reset(self):
        self.page.goto(self.url)

    def add_array_value(self, field: str, value: str):
        """
        Used when an array widget is being used, without choices.
        """
        self.page.locator(
            f"[data-uitest={field}_array_widget] [data-uitest=add_array_item_button]"  # noqa: E501
        ).click()

        self.page.locator(f"[data-uitest={field}_array_widget] input").fill(
            value
        )

    def add_array_choice(self, field: str, option: str):
        """
        Used when an array widget is being used, with choices.
        """
        self.page.locator(
            f"[data-uitest={field}_array_widget] [data-uitest=add_array_item_button]"  # noqa: E501
        ).click()

        self.page.locator(
            f"[data-uitest={field}_array_widget] select"
        ).select_option(option)

    def select_value(self, field: str, option: str):
        """
        Used when a non-array widget is being used, with choices.
        """
        self.page.locator(f"select[name={field}]").select_option(option)

    def submit_form(self, expected_status: int = 201):
        with self.page.expect_response(
            lambda response: response.url
            == f"{BASE_URL}/api/tables/{self.tablename}/"
            and response.request.method == "POST"
            and response.status == expected_status
        ):
            self.create_button.click()


###############################################################################


class Nav:
    def __init__(self, page: Page):
        self.page = page
        self.nav_dropdown_button = page.locator(
            'a[data-uitest="nav_dropdown_button"]'
        )
        self.logout_button = page.locator('a[data-uitest="logout_button"]')

    def logout(self):
        self.nav_dropdown_button.click()
        self.page.on("dialog", lambda dialog: dialog.accept())

        with self.page.expect_response(
            lambda response: response.url == f"{BASE_URL}/public/logout/"
            and response.request.method == "POST"
            and response.status == 200
        ):
            self.logout_button.click()


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = f"{BASE_URL}/#/"
        self.nav = Nav(page=page)

    def reset(self):
        self.page.goto(self.url)


###############################################################################


class FormPage:
    def __init__(self, page: Page, form_slug: str):
        self.page = page
        self.url = f"{BASE_URL}/#/forms/{form_slug}"
        self.submit_button = page.locator(
            "button[data-uitest=submit_custom_form_button]"
        )

    def reset(self):
        self.page.goto(self.url)

    def submit_form(self):
        self.submit_button.click()
