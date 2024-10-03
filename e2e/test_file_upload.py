from playwright.sync_api import Page

from piccolo_admin.example.tables import Director

from .pages import EditRowPage, LoginPage


def test_file_upload(page: Page, dev_server):
    """
    Make sure files can be uploaded, and the database is updated accordingly.
    """
    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    director = Director.objects().first().run_sync()
    assert director

    edit_row_page = EditRowPage(
        page=page,
        tablename=Director._meta.tablename,
        row_id=str(director.id),
    )
    edit_row_page.reset()

    page.locator('input[type="file"]').set_input_files(
        "./e2e/upload/piccolo.jpg"
    )

    edit_row_page.save()

    director.refresh().run_sync()
    assert director.photo.startswith("piccolo")
    assert director.photo.endswith(".jpg")
