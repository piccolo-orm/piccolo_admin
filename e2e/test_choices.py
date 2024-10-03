from playwright.sync_api import Page

from piccolo_admin.example.tables import Choices

from .pages import AddRowPage, LoginPage


def test_choices(page: Page, dev_server):
    """
    Make sure choices work as expected.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    add_row_page = AddRowPage(
        page=page,
        tablename=Choices._meta.tablename,
    )
    add_row_page.reset()

    # Let Vue JS finish loading
    page.wait_for_timeout(1000)

    for field in ("array", "array_null"):
        add_row_page.add_array_choice(
            field=field,
            option=Choices.ArrayChoices.a.value,
        )

    for field in ("date", "date_null"):
        add_row_page.select_value(
            field=field,
            option=Choices.DateChoices.early.value.strftime("%Y-%m-%d"),
        )

    for field in ("integer", "integer_null"):
        add_row_page.select_value(
            field=field,
            option=str(Choices.IntegerChoices.low.value),
        )

    for field in ("varchar", "varchar_null"):
        add_row_page.select_value(
            field=field,
            option=Choices.VarcharChoices.a.value,
        )

    add_row_page.submit_form()

    choices_in_db = Choices.select(
        Choices.all_columns(exclude=[Choices.id])  # type: ignore
    ).run_sync()

    assert {
        "array": [Choices.ArrayChoices.a.value],
        "array_null": [Choices.ArrayChoices.a.value],
        "date": Choices.DateChoices.early.value,
        "date_null": Choices.DateChoices.early.value,
        "integer": Choices.IntegerChoices.low.value,
        "integer_null": Choices.IntegerChoices.low.value,
        "varchar": Choices.VarcharChoices.a.value,
        "varchar_null": Choices.VarcharChoices.a.value,
    } in choices_in_db
