from playwright.sync_api import Page

from piccolo_admin.example.forms.csv import FORM as CSV_FORM
from piccolo_admin.example.forms.enum import FORM as ENUM_FORM
from piccolo_admin.example.forms.image import FORM as IMAGE_FORM
from piccolo_admin.example.forms.nullable import FORM as NULLABLE_FORM

from .conftest import BASE_URL
from .pages import FormPage, LoginPage


def test_csv_form(page: Page, dev_server):
    """
    Make sure a CSV file can be downloaded from a custom form.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    form_page = FormPage(
        page=page,
        form_slug=CSV_FORM.slug,
    )
    form_page.reset()

    page.locator('input[name="director_name"]').fill("George Lucas")

    # Make sure a file was downloaded
    # In the future we could also check the contents, but a unit test currently
    # does this.
    with page.expect_download() as download_info:
        form_page.submit_form()

    download = download_info.value
    assert download.suggested_filename == "director_movies.csv"


def test_image_form(page: Page, dev_server):
    """
    Make sure an image file can be downloaded from a custom form.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    form_page = FormPage(
        page=page,
        form_slug=IMAGE_FORM.slug,
    )
    form_page.reset()

    page.locator('input[name="date"]').fill("2024-10-01")

    # Make sure a file was downloaded:
    with page.expect_download() as download_info:
        form_page.submit_form()

    download = download_info.value
    assert download.suggested_filename == "movie_listings.jpg"


def test_nullable_form(page: Page, dev_server):
    """
    Make sure a form with nullable fields can be submitted successfully.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    form_page = FormPage(
        page=page,
        form_slug=NULLABLE_FORM.slug,
    )
    form_page.reset()

    with page.expect_response(
        lambda response: response.url
        == f"{BASE_URL}/api/forms/nullable-fields/"
        and response.request.method == "POST"
        and response.status == 200
    ):
        form_page.submit_form()


def test_form_enum(page: Page, dev_server):
    """
    Make sure custom forms support the usage of Enum's.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    form_page = FormPage(
        page=page,
        form_slug=ENUM_FORM.slug,
    )
    form_page.reset()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="email"]').fill("piccolo@example.com")
    page.locator('select[name="permissions"]').select_option("admissions")

    with page.expect_response(
        lambda response: response.url == f"{BASE_URL}/api/forms/enum-form/"
        and response.request.method == "POST"
        and response.status == 200
    ):
        form_page.submit_form()
