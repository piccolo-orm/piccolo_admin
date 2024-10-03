import csv
import os
import tempfile

from playwright.sync_api import Page

from piccolo_admin.example.tables import Movie

from .pages import LoginPage, RowListingPage


def test_csv_download(page: Page, dev_server):
    """
    Make sure we can download a CSV file from the row listing page.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = RowListingPage(page=page, tablename=Movie._meta.tablename)
    test_page.reset()

    # Give Vue JS time to finish setting up the page.
    page.wait_for_timeout(1000)

    with page.expect_download() as download_info:
        test_page.show_csv_modal()
        test_page.csv_modal.click_download()

    path = os.path.join(tempfile.gettempdir(), "test.csv")

    download_info.value.save_as(path)

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        data = [i for i in reader]

    assert {i["name"] for i in data} == {
        i for i in Movie.select(Movie.name).output(as_list=True).run_sync()
    }
