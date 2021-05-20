"""
get_single
    Anyone
put_single
    Only superusers can create other superusers. Admins can create other
    admins, and non admin.
patch_single
    Only superusers can create other superusers, and set super users as
    inactive.
delete_single
post_single
get_all
    No restrictions
delete_all

get_references
    No restrictions
get_ids
    No restrictions
get_new
    No restrictions
get_schema
    No restrictions
get_count
    No restrictions
"""


from __future__ import annotations
import typing as t

from piccolo_api.crud.validators import Validators
from starlette.exceptions import HTTPException

if t.TYPE_CHECKING:
    from piccolo.apps.user.tables import BaseUser
    from piccolo_api.crud.endpoints import PiccoloCRUD
    from starlette.requests import Request


def validate_delete_single(
    piccolo_crud: PiccoloCRUD, request: Request, auth_table: BaseUser, **kwargs
):
    # request.user.user_id
    raise HTTPException(
        status_code=403, detail="The user doesn't have permissios for this."
    )


def validate_delete_all(
    piccolo_crud: PiccoloCRUD, request: Request, auth_table: BaseUser, **kwargs
):
    pass


def validate_get_all(
    piccolo_crud: PiccoloCRUD, request: Request, auth_table: BaseUser, **kwargs
):
    raise HTTPException(
        status_code=403, detail="The user doesn't have permissions for this."
    )


###############################################################################


USER_VALIDATORS = Validators(
    delete_single=[validate_delete_single],
    delete_all=[validate_delete_all],
    get_all=[validate_get_all],
)
