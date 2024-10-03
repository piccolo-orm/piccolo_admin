from playwright.sync_api import Page

from piccolo_admin.example.tables import Movie

from .pages import LoginPage, RowListingPage


def test_match(page: Page, dev_server):
    """
    Make sure that the filters can specify how to match text values - for
    example that the Movie name starts with 'Star'.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = RowListingPage(page=page, tablename=Movie._meta.tablename)
    test_page.reset()

    # Give Vue JS time to finish setting up the page.
    page.wait_for_timeout(1000)

    test_page.open_filter_sidebar()

    field_name = "name"

    name_input = test_page.filter_sidebar.get_input(name=field_name)
    name_input.type("Star Wars")

    match_selector = test_page.filter_sidebar.get_match_selector(
        name=field_name
    )
    match_selector.select_option("starts")

    # Submit the form, and wait for the API response
    with page.expect_response(
        lambda response: "/tables/movie/?" in response.url
    ) as response_info:
        test_page.filter_sidebar.submit_form()

    # Make sure the correct GET params were sent
    assert f"{field_name}__match=starts" in response_info.value.url
    assert f"{field_name}=Star+Wars" in response_info.value.url

    # Make sure the data was filtered correctly.
    # There's a movie called `Rogue One: Star Wars`, which shouldn't be
    # returned.
    for movie_name in [i["name"] for i in response_info.value.json()["rows"]]:
        assert movie_name.startswith("Star Wars")
