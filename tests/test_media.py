import os
import tempfile
import uuid
from unittest import TestCase
from unittest.mock import MagicMock, patch

from piccolo_admin.media.storage import LocalMediaStorage


class TestLocalMediaStorage(TestCase):
    @patch("piccolo_admin.media.storage.uuid")
    def test_store_file(self, uuid_module: MagicMock):
        """
        Make sure we can store files, and retrieve them.
        """
        uuid_module.uuid4.return_value = uuid.UUID(
            "fd0125c7-8777-4976-83c1-81605d5ab155"
        )

        media_path = tempfile.gettempdir()

        storage = LocalMediaStorage(media_path=media_path, media_url="/media/")

        with open(
            os.path.join(os.path.dirname(__file__), "files/bulb.jpg"), "rb"
        ) as test_file:
            # Store the file
            file_id = storage.store_file_sync(test_file)
            self.assertTrue(file_id in os.listdir(media_path))

            # Retrive the URL for the file
            url = storage.get_file_url_sync(file_id)
            self.assertEqual(
                url, "/media/bulb-fd0125c7-8777-4976-83c1-81605d5ab155.jpg"
            )
