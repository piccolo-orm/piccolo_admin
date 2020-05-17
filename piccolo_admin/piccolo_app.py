"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="piccolo_admin",
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY, "piccolo_migrations"
    ),
    table_classes=[],
    migration_dependencies=[
        "piccolo_api.session_auth.piccolo_app",
        "piccolo.apps.user.piccolo_app",
    ],
    commands=[],
)
