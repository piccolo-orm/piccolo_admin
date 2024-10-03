from playwright.sync_api import Page

from piccolo_admin.example.forms.csv import FORM as CSV_FORM
from piccolo_admin.example.forms.image import FORM as IMAGE_FORM

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
