import pytest
import time
from subprocess import Popen, PIPE
from http.client import HTTPConnection

from playwright.sync_api import Playwright, sync_playwright


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
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click #user
    page.locator("#user").click()
    # Click text=Log out
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.locator("text=Log out").click()
    # ---------------------
    context.close()
    browser.close()


def test_row_listing_filter(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=director
    page.locator("text=director").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Click text=Show filters
    page.locator("text=Show filters").click()
    # Click input[name="name"]
    page.locator('input[name="name"]').click()
    # Fill input[name="name"]
    page.locator('input[name="name"]').fill("Howard")
    # Press Enter
    page.locator('input[name="name"]').press("Enter")
    # Click text=Clear filters
    page.locator("text=Clear filters").click()
    # Click input[name="name"]
    page.locator('input[name="name"]').click()
    # Fill input[name="name"]
    page.locator('input[name="name"]').fill("Ron")
    # Click text=Apply
    page.locator("text=Apply").click()
    # Click text=Clear filters
    page.locator("text=Clear filters").click()
    # Click text=Close
    page.locator("text=Close").click()
    # Click span:has-text("Sort")
    page.locator("span", has_text="Sort").click()
    # Select ascending
    page.locator('select[name="ordering"]').select_option("ascending")
    # Click button:has-text("Sort")
    page.locator("button", has_text="Sort").click()
    page.wait_for_timeout(2000)
    page.locator("#user").click()
    # Click text=Log out
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("text=Log out").click()
    page.wait_for_url("http://localhost:8000/#/login?nextURL=%2F")
    # ---------------------
    context.close()
    browser.close()


def test_custom_form(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=Business email form
    page.locator("text=Business email form").click()
    page.wait_for_url("http://localhost:8000/#/forms/business-email-form")
    # Click input[name="email"]
    page.locator('input[name="email"]').click()
    # Fill input[name="email"]
    page.locator('input[name="email"]').fill("director@director.com")
    # Click input[name="title"]
    page.locator('input[name="title"]').click()
    # Click text=Piccolo Admin piccolo Back Business email form Send an email to a business assoc
    page.locator(
        "text=Piccolo Admin piccolo Back Business email form Send an email to a business assoc"
    ).click()
    # Click input[name="title"]
    page.locator('input[name="title"]').click()
    # Fill input[name="title"]
    page.locator('input[name="title"]').fill("Hello")
    # Click input[name="content"]
    page.locator('input[name="content"]').click()
    # Fill input[name="content"]
    page.locator('input[name="content"]').fill("Hello from Piccolo Admin")
    # Click button:has-text("Submit")
    page.locator('button:has-text("Submit")').click()
    # Click text=Back >> nth=0
    page.locator("text=Back").first.click()
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=Booking form
    page.locator("text=Booking form").click()
    page.wait_for_url("http://localhost:8000/#/forms/booking-form")
    # Click input[name="email"]
    page.locator('input[name="email"]').click()
    # Fill input[name="email"]
    page.locator('input[name="email"]').fill("customer@customer.com")
    # Click input[name="name"]
    page.locator('input[name="name"]').click()
    # Fill input[name="name"]
    page.locator('input[name="name"]').fill("Bob")
    # Click input[name="notes"]
    page.locator('input[name="notes"]').click()
    # Fill input[name="notes"]
    page.locator('input[name="notes"]').fill("Star Wars please")
    # Click button:has-text("Submit")
    page.locator('button:has-text("Submit")').click()
    # Click text=Back >> nth=0
    page.locator("text=Back").first.click()
    page.wait_for_timeout(2000)
    page.locator("#user").click()
    # Click text=Log out
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("text=Log out").click()
    page.wait_for_url("http://localhost:8000/#/login?nextURL=%2F")
    # ---------------------
    context.close()
    browser.close()


def test_file_upload(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=director
    page.locator("text=director").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Click a:has-text("8")
    page.locator('a:has-text("8")').click()
    page.wait_for_url("http://localhost:8000/#/director/8")
    # Upload piccolo.jpg
    page.locator('input[type="file"]').set_input_files(
        "./e2e/upload/piccolo.jpg"
    )
    # Click text=Save
    page.locator("text=Save").click()
    # Click text=Back
    page.locator("text=Back").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Click image link
    page.locator("text=piccolo-").click()
    # Close image preview
    page.locator("div#media_viewer div.top_bar p.close").click()
    # ---------------------
    context.close()
    browser.close()


def test_bulk_update(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=director
    page.locator("text=director").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Check text=id Name Gender Photo >> input[type="checkbox"]
    page.locator('text=id Name Gender Photo >> input[type="checkbox"]').check()
    # Click a:has-text("Update 8 rows")
    page.locator('a:has-text("Update 8 rows")').click()
    # Select gender
    page.locator('select[name="property"]').select_option("gender")
    # Select f
    page.locator('select[name="gender"]').select_option("f")
    # Click button:has-text("Update")
    page.locator('button:has-text("Update")').click()
    # Click #user
    page.wait_for_timeout(2000)
    page.locator("#user").click()
    # Click text=Log out
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("text=Log out").click()
    page.wait_for_url("http://localhost:8000/#/login?nextURL=%2F")
    # ---------------------
    context.close()
    browser.close()


def test_table_crud(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://localhost:8000/#/login?nextURL=%2F
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    # Click input[name="username"]
    page.locator('input[name="username"]').click()
    # Fill input[name="username"]
    page.locator('input[name="username"]').fill("piccolo")
    # Press Tab
    page.locator('input[name="username"]').press("Tab")
    # Fill input[name="password"]
    page.locator('input[name="password"]').fill("piccolo123")
    # Press Enter
    page.locator('input[name="password"]').press("Enter")
    page.wait_for_url("http://localhost:8000/#/")
    # Click text=director
    page.locator("text=director").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Click a:has-text("8")
    page.locator('a:has-text("8")').click()
    page.wait_for_url("http://localhost:8000/#/director/8")
    # Click text=Piccolo Admin piccolo Back Edit director Name Years Nominated Which years this d
    page.locator(
        "text=Piccolo Admin piccolo Back Edit director Name Years Nominated Which years this d"
    ).click()
    # Fill input[type="text"] >> nth=2
    page.locator('input[type="text"]').nth(2).fill("Ronald William Howard2009")
    # Press z with modifiers
    page.locator('input[type="text"]').nth(2).press("Control+z")
    # Click input[name="name"]
    page.locator('input[name="name"]').click()
    # Fill input[name="name"]
    page.locator('input[name="name"]').fill("Ronald William Howard")
    # Click text=Save
    page.locator("text=Save").click()
    # Click text=Back
    page.locator("text=Back").click()
    page.wait_for_url("http://localhost:8000/#/director")
    # Click text=Add Row
    page.locator("text=Add Row").click()
    page.wait_for_url("http://localhost:8000/#/director/add")
    # Click input[name="name"]
    page.locator('input[name="name"]').click()
    # Fill input[name="name"]
    page.locator('input[name="name"]').fill("Emerald Fennell")
    # Click text=AddAdd
    page.locator("text=AddAdd").click()
    # Click text=RemoveAddAdd >> input[type="text"]
    page.locator('text=RemoveAddAdd >> input[type="text"]').click()
    # Fill text=RemoveAddAdd >> input[type="text"]
    page.locator('text=RemoveAddAdd >> input[type="text"]').fill("2020")
    # Select f
    page.locator('select[name="gender"]').select_option("f")
    # Click text=Create
    page.locator("text=Create").click()
    # Click text=Back
    page.locator("text=Back").click()
    page.wait_for_timeout(3000)
    page.wait_for_url("http://localhost:8000/#/director")
    # Check text=5Irvin Kershner Male >> input[type="checkbox"]
    page.locator('text=5Irvin Kershner Male >> input[type="checkbox"]').check()
    # Click text=Delete 1 rows
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("text=Delete 1 rows").click()
    # Check text=id Name Gender Photo >> input[type="checkbox"]
    page.locator('text=id Name Gender Photo >> input[type="checkbox"]').check()
    # Click text=Delete 8 rows
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("text=Delete 8 rows").click()
    # wait for rows deletion
    page.wait_for_timeout(2000)
    page.locator("#user").click()
    # Click text=Log out
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.locator("text=Log out").click()
    # ---------------------
    context.close()
    browser.close()
