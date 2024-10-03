from playwright.sync_api import Page

from piccolo_admin.example.tables import Movie

from .pages import LoginPage, RowListingPage


def test_operator(page: Page, dev_server):
    """
    Make sure that the filters can specify the operator to use - for
    example that the Movie genre doesn't include 'Fantasy'.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = RowListingPage(page=page, tablename=Movie._meta.tablename)
    test_page.reset()

    # Give Vue JS time to finish setting up the page.
    page.wait_for_timeout(1000)

    test_page.open_filter_sidebar()

    field_name = "genre"

    name_input = test_page.filter_sidebar.get_input(name=field_name)
    name_input.select_option("Fantasy")

    operator_selector = test_page.filter_sidebar.get_operator_selector(
        name=field_name
    )
    operator_selector.select_option("ne")

    # Submit the form, and wait for the API response
    with page.expect_response(
        lambda response: "/tables/movie/?" in response.url
    ) as response_info:
        test_page.filter_sidebar.submit_form()

    # Make sure the correct GET params were sent
    assert f"{field_name}__operator=ne" in response_info.value.url
    assert (
        f"{field_name}={Movie.Genre.fantasy.value}" in response_info.value.url
    )

    # Make sure the data was filtered correctly.
    # Fantasy movies shouldn't be returned.
    genres = [i["genre"] for i in response_info.value.json()["rows"]]
    assert Movie.Genre.fantasy.value not in genres
    assert Movie.Genre.sci_fi.value in genres
