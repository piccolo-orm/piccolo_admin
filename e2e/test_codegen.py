"""
These are auto generated tests.

https://playwright.dev/docs/codegen
"""

from playwright.sync_api import Playwright


def test_row_listing_filter(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').click()
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="username"]').press("Tab")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director", exact=True).click()
    page.get_by_role("link", name="Show filters").click()
    name_input = page.locator('.filter_wrapper input[name="name"]')
    name_input.click()
    name_input.fill("Howard")
    name_input.press("Enter")
    page.get_by_role("button", name="Clear filters").click()
    name_input.click()
    name_input.fill("ron")
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="Clear filters").click()
    page.get_by_text("Close").click()
    page.locator("a[data-uitest=sort_button]").click()
    page.locator('select[name="column"]').select_option("name")
    page.locator('select[name="ordering"]').select_option(label="Ascending")
    page.get_by_role("button", name="Sort").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log Out").click()
    # ---------------------
    context.close()
    browser.close()


def test_custom_form(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="Booking form").click()
    page.locator('input[name="email"]').fill("customer@customer.com")
    page.locator('input[name="name"]').fill("Bob")
    page.locator('input[name="tickets"]').fill("2")

    # We can't fill hidden elements - so need to do this instead:
    page.evaluate(
        'document.querySelector("input[name=starts_at]").setAttribute("value", "2024-10-01T12:00:00")'  # noqa: E501
    )

    page.locator('input[name="notes"]').fill("Hello from Piccolo Admin")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("link", name="Back to home page").click()
    page.get_by_title("piccolo").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_text("Log Out").click()
    # ---------------------
    context.close()
    browser.close()


def test_bulk_update(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="director", exact=True).click()
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
    page.get_by_text("Log Out").click()
    # ---------------------
    context.close()
    browser.close()


def test_custom_links(playwright: Playwright, dev_server) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context(record_video_dir="videos/")
    # Open new page
    page = context.new_page()
    page.goto("http://localhost:8000/#/login?nextURL=%2F")
    page.locator('input[name="username"]').fill("piccolo")
    page.locator('input[name="password"]').fill("piccolo123")
    page.locator('input[name="password"]').press("Enter")
    page.get_by_role("link", name="Top Movies").click()
    page.get_by_role("link", name="7", exact=True).click()
    page.get_by_role("link", name="piccolo", exact=True).click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("link", name="Log Out", exact=True).click()
    # ---------------------
    context.close()
    browser.close()
