import time
from http.client import HTTPConnection
from subprocess import PIPE, Popen

import pytest
from playwright.sync_api import Playwright


@pytest.fixture
def dev_server():
    """
    Running dev server and Playwright test in parallel.
    More info https://til.simonwillison.net/pytest/playwright-pytest
    """
    process = Popen(
        ["python", "-m", "piccolo_admin.example"],
        stdout=PIPE,
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection("localhost:8000")
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield process
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1

    if not retries:
        raise RuntimeError("Failed to start http server")
    else:
        process.terminate()
        process.wait()


def test_login_logout(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_row_listing_filter(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director").click()
    page.get_by_role("link", name="Show filters").click()
    page.locator('input[name="name"]').click()
    page.locator('input[name="name"]').fill("Howard")
    page.locator('input[name="name"]').press("Enter")
    page.get_by_role("button", name="Clear filters").click()
    page.locator('input[name="name"]').click()
    page.locator('input[name="name"]').fill("ron")
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="Clear filters").click()
    page.get_by_text("Close").click()
    page.get_by_role("link", name="Sort").click()
    page.locator('select[name="property"]').select_option("name")
    page.locator('select[name="ordering"]').select_option("ascending")
    page.get_by_role("button", name="Sort").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_custom_form(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="Business email form").click()
    page.locator('input[name="email"]').click()
    page.locator('input[name="email"]').fill("director@director.com")
    page.locator('input[name="content"]').click()
    page.locator('input[name="content"]').fill("Hello from Piccolo Admin")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("paragraph").filter(has_text="Back").get_by_role(
        "link", name="Back"
    ).click()
    page.get_by_role("link", name="Booking form").click()
    page.locator('input[name="email"]').click()
    page.locator('input[name="email"]').fill("customer@customer.com")
    page.locator('input[name="name"]').click()
    page.locator('input[name="name"]').fill("Bob")
    page.locator('input[name="notes"]').click()
    page.locator('input[name="notes"]').fill("Hello from Piccolo Admin")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("link", name="Back to home page").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_file_upload(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director").click()
    page.get_by_role("link", name="8").click()
    page.locator('input[type="file"]').click()
    page.locator('input[type="file"]').set_input_files(
        "./e2e/upload/piccolo.jpg"
    )
    page.get_by_text(
        "Piccolo Admin piccolo Back Edit director Name Years Nominated Which years this d"
    ).click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("link", name="Back").click()
    page.get_by_text("piccolo-").click()
    page.locator("#media_viewer div").filter(
        has_text="File: piccolo-"
    ).get_by_role("link").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_bulk_update(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director").click()
    page.locator("th").first.click()
    page.get_by_role("row", name="id Name Gender Photo").get_by_role(
        "checkbox"
    ).check()
    page.get_by_role("link", name="Update 8 rows").click()
    page.locator('select[name="property"]').select_option("gender")
    page.locator('select[name="gender"]').select_option("f")
    page.get_by_role("button", name="Update").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_table_crud(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:3000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director").click()
    page.get_by_role("cell", name="8").click()
    page.get_by_role("link", name="8").click()
    page.locator('input[name="name"]').click()
    page.locator('input[name="name"]').fill("Ronald William Howard")
    page.locator('input[name="name"]').press("Enter")
    page.get_by_role("link", name="Back").click()
    page.get_by_role("row", name="id Name Gender Photo").get_by_role(
        "checkbox"
    ).check()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("link", name="Delete 8 rows").click()
    page.get_by_role("link", name="Add Row").click()
    page.locator('input[name="name"]').click()
    page.locator('input[name="name"]').fill("Emerald Fennell")
    page.get_by_role("link", name="Add Add").first.click()
    page.get_by_role("listitem").filter(has_text="Remove").get_by_role(
        "textbox"
    ).click()
    page.get_by_role("listitem").filter(has_text="Remove").get_by_role(
        "textbox"
    ).fill("2022")
    page.get_by_role("combobox").select_option("m")
    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Back").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log out").click()
    # ---------------------
    context.close()
    browser.close()
