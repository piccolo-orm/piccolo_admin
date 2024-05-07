from __future__ import annotations

import typing as t


def convert_enum_to_choices(enum_data: t.Any) -> t.Dict[str, t.Any]:
    choices = {}
    for item in enum_data:
        choices[item.name] = {
            "display_name": item.name,
            "value": item.value,
        }
    return choices
