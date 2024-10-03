from playwright.sync_api import Page

from piccolo_admin.example.tables import Constraints, ConstraintTarget

from .pages import EditRowPage, LoginPage


def test_constraints(page: Page, dev_server):
    """
    Make sure that deleting rows with constraints is handled gracefully,
    showing an error message.
    """
    constraint_target = ConstraintTarget({ConstraintTarget.name: "Test"})
    constraint_target.save().run_sync()

    constraint = Constraints({Constraints.restrict: constraint_target})
    constraint.save().run_sync()

    login_page = LoginPage(page=page)
    login_page.reset()
    login_page.login()

    test_page = EditRowPage(
        page=page,
        tablename=ConstraintTarget._meta.tablename,
        row_id=str(constraint_target.id),
    )
    test_page.reset()
    test_page.delete()
    test_page.error_list.check_error(
        error="Database error: FOREIGN KEY constraint failed"
    )
