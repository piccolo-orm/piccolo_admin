from playwright.sync_api import Page

from piccolo_admin.example.forms.csv import FORM
from piccolo_admin.example.tables import Director

from .pages import FormPage, LoginPage


def test_custom_form(page: Page, dev_server):
    """
    Make sure files can be downloaded from a custom form.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    director = Director.objects().first().run_sync()
    assert director

    form_page = FormPage(
        page=page,
        form_slug=FORM.slug,
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
