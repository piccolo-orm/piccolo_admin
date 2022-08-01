import os
import shutil
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

        media_path = os.path.join(tempfile.gettempdir(), "piccolo-admin-media")

        if os.path.exists(media_path):
            shutil.rmtree(media_path)

        os.mkdir(media_path)

        storage = LocalMediaStorage(media_path=media_path, media_url="/media/")

        with open(
            os.path.join(os.path.dirname(__file__), "test_files/bulb.jpg"),
            "rb",
        ) as test_file:
            # Store the file
            file_id = storage.store_file_sync(
                file_name="bulb.jpg", file=test_file
            )

            # Make sure the file was stored.
            self.assertTrue(file_id in os.listdir(media_path))

            # Make sure the permissions are correct
            self.assertEqual(
                oct(os.stat(os.path.join(media_path, file_id)).st_mode)[-3:],
                "640",
            )

            # Retrieve the URL for the file
            url = storage.generate_file_url_sync(file_id)
            self.assertEqual(
                url, "/media/bulb-fd0125c7-8777-4976-83c1-81605d5ab155.jpg"
            )


class TestGenerateFileID(TestCase):
    def setUp(self) -> None:
        self.media_path = tempfile.gettempdir()
        self.storage = LocalMediaStorage(
            media_path=self.media_path, media_url="/media/"
        )

    def test_starts_with_period(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_id(file_name=".private_file.jpeg")

        self.assertEqual(
            str(manager.exception), "File names must not start with a period."
        )

    def test_double_period(self):
        """
        A file_name containing a double period shoudn't be allowed, as it
        could potentially be used to traverse the file system.
        """
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_id(file_name="test/../file.jpeg")

        self.assertEqual(
            str(manager.exception), "File names must not contain '..'."
        )

    def test_empty_file_name(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_id(file_name="")

        self.assertEqual(
            str(manager.exception), "The file name can't be empty."
        )

    def test_allowed_extensions(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_id(
                file_name="test.abcdefghijklmonpqrstuvwxyz123"
            )

        self.assertEqual(
            str(manager.exception), "This file type isn't allowed."
        )

    def test_allowed_characters(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_id(file_name="@{£}%^*jpeg")

        self.assertEqual(
            str(manager.exception), "'@' is not allowed in the filename."
        )

    @patch("piccolo_admin.media.storage.uuid")
    def test_long_file_name(self, uuid_module: MagicMock):
        """
        Make sure that really long file names are truncated.
        """
        uuid_module.uuid4.return_value = uuid.UUID(
            "fd0125c7-8777-4976-83c1-81605d5ab155"
        )

        truncated_file_id = self.storage.generate_file_id(
            file_name="".join("a" for _ in range(200)) + ".jpg"
        )
        self.assertEqual(
            truncated_file_id,
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-fd0125c7-8777-4976-83c1-81605d5ab155.jpg",  # noqa: E501
        )
