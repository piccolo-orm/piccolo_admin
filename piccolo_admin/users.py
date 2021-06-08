from __future__ import annotations
from json import JSONDecodeError
import typing as t

from piccolo_api.crud.validators import Validators
from piccolo_api.shared.auth.user import User
from starlette.exceptions import HTTPException

if t.TYPE_CHECKING:
    from piccolo_api.crud.endpoints import PiccoloCRUD
    from starlette.requests import Request


def is_self(piccolo_crud: PiccoloCRUD, request: Request):
    try:
        user_id = request.path_params.get("row_id")
    except TypeError:
        return

    user: User = request.user
    if not user_id == user.user_id:
        raise HTTPException(
            status_code=403, detail="You can't edit other users.",
        )


def is_admin(piccolo_crud: PiccoloCRUD, request: Request):
    user: User = request.user
    if not user.piccolo_user.admin:
        raise HTTPException(
            status_code=403, detail="The user is not an admin.",
        )


def is_superuser(piccolo_crud: PiccoloCRUD, request: Request):
    user: User = request.user
    if not user.superuser:
        raise HTTPException(
            status_code=403, detail="The user is not a superuser.",
        )


async def can_change_superuser_flag(
    piccolo_crud: PiccoloCRUD, request: Request
):
    """
    Check if the user is allowed to change someone to a superuser.
    """
    user: User = request.user

    try:
        body = await request.json()
    except JSONDecodeError:
        body = await request.form()

    if (
        body.get("superuser") in [True, "true"]
        and not user.piccolo_user.superuser
    ):
        raise HTTPException(
            status_code=403,
            detail="Only superusers can create other superusers",
        )


async def can_change_active_flag(piccolo_crud: PiccoloCRUD, request: Request):
    user: User = request.user

    try:
        body = await request.json()
    except JSONDecodeError:
        body = await request.form()

    if (
        body.get("active") in [False, "false"]
        and not user.piccolo_user.superuser
    ):
        raise HTTPException(
            status_code=403, detail="Only superusers can make users inactive",
        )


async def can_change_admin_flag(piccolo_crud: PiccoloCRUD, request: Request):
    user: User = request.user

    try:
        body = await request.json()
    except JSONDecodeError:
        body = await request.form()

    if (
        body.get("admin") in [False, "false"]
        and not user.piccolo_user.superuser
    ):
        raise HTTPException(
            status_code=403,
            detail="Only superusers can make users non-admins",
        )


def any_pass(*validators: t.Callable):
    """
    If at least one of the validators doesn't raise an exception, the validator
    passes.
    """

    def check(piccolo_crud: PiccoloCRUD, request: Request, **kwargs):
        max_exceptions = len(validators)
        exception_count = 0
        for validator in validators:
            try:
                validator(piccolo_crud, request, **kwargs)
            except Exception as exception:
                exception_count += 1
                if exception_count == max_exceptions:
                    raise exception

    return check


###############################################################################


USER_VALIDATORS = Validators(
    get_single=[],
    put_single=[can_change_superuser_flag],
    # Only superusers can create other superusers. Admins can create other
    # admins, and non admin.
    patch_single=[
        can_change_superuser_flag,
        can_change_active_flag,
        can_change_admin_flag,
        any_pass(is_superuser, is_self),
    ],
    # Only superusers can create other superusers, and set super users as
    # inactive.
    post_single=[can_change_superuser_flag],
    delete_single=[is_superuser],
    delete_all=[is_superuser],
    get_all=[],
    get_references=[],
    get_ids=[],
    get_new=[],
    get_schema=[],
    get_count=[],
)
