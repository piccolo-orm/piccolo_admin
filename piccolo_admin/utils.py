from __future__ import annotations

from typing import Any


def convert_enum_to_choices(enum_data: Any) -> dict[str, Any]:
    choices = {}
    for item in enum_data:
        choices[item.name] = {
            "display_name": item.name.replace('_', ' '),
            "value": item.value,
        }
    return choices
