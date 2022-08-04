import asyncio
import os
import shutil
import tempfile
import uuid
from unittest import TestCase
from unittest.mock import MagicMock, patch

from piccolo.columns.column_types import Array, Integer
from piccolo.table import create_db_tables_sync, drop_db_tables_sync

from piccolo_admin.example import Director, Movie, Studio
from piccolo_admin.media.local import LocalMediaStorage
from piccolo_admin.media.s3 import S3MediaStorage


class TestGenerateFileID(TestCase):
    def setUp(self) -> None:
        self.media_path = tempfile.gettempdir()
        self.storage = LocalMediaStorage(
            column=Movie.poster, media_path=self.media_path
        )

    def test_starts_with_period(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(file_name=".private_file.jpeg")

        self.assertEqual(
            str(manager.exception), "File names must not start with a period."
        )

    def test_double_period(self):
        """
        A file_name containing a double period shouldn't be allowed, as it
        could potentially be used to traverse the file system.
        """
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(file_name="test..file.jpeg")

        self.assertEqual(
            str(manager.exception), "File names must not contain '..'."
        )

    def test_empty_file_name(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(file_name="")

        self.assertEqual(
            str(manager.exception), "The file name can't be empty."
        )

    def test_allowed_extensions(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(
                file_name="test.abcdefghijklmonpqrstuvwxyz123"
            )

        self.assertEqual(
            str(manager.exception), "This file type isn't allowed."
        )

    def test_allowed_characters(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(file_name="@{£}%^*jpeg")

        self.assertEqual(
            str(manager.exception), "'@' is not allowed in the filename."
        )

    def test_no_extension(self):
        with self.assertRaises(ValueError) as manager:
            self.storage.generate_file_key(file_name="test")

        self.assertEqual(str(manager.exception), "The file has no extension.")

    @patch("piccolo_admin.media.base.uuid")
    def test_long_file_name(self, uuid_module: MagicMock):
        """
        Make sure that really long file names are truncated.
        """
        uuid_module.uuid4.return_value = uuid.UUID(
            "fd0125c7-8777-4976-83c1-81605d5ab155"
        )

        truncated_file_key = self.storage.generate_file_key(
            file_name="".join("a" for _ in range(200)) + ".jpg"
        )
        self.assertEqual(
            truncated_file_key,
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-fd0125c7-8777-4976-83c1-81605d5ab155.jpg",  # noqa: E501
        )


class TestInit(TestCase):
    def test_unsupported_column(self):
        """
        We only allow media columns which can store strings in them.
        """
        with self.assertRaises(ValueError) as manager:
            LocalMediaStorage(column=Movie.rating, media_path="/tmp/")

        self.assertEqual(
            str(manager.exception),
            "The column must be a `Varchar`, `Text`, or `Array`.",
        )

    def test_arrays(self):
        """
        Arrays are allowed, but only if the ``base_column`` can store strings.
        """
        with self.assertRaises(ValueError) as manager:
            LocalMediaStorage(
                column=Array(base_column=Integer()), media_path="/tmp/"
            )

        self.assertEqual(
            str(manager.exception),
            "The column must be a `Varchar`, `Text`, or `Array`.",
        )

        # This should raise no exceptions, as it's an Array of Varchar.
        LocalMediaStorage(column=Movie.poster, media_path="/tmp/")


class TestGetFileKeysFromDB(TestCase):
    def setUp(self):
        create_db_tables_sync(Movie, Director, Studio)

    def tearDown(self):
        drop_db_tables_sync(Movie, Director, Studio)

    def test_get_file_keys_from_db(self):
        Movie.insert(
            Movie(poster="image-1.jpg"),
            Movie(poster="image-2.jpg"),
            Movie(poster="image-3.jpg"),
        ).run_sync()

        storage = LocalMediaStorage(column=Movie.poster, media_path="/tmp/")

        response = asyncio.run(storage.get_file_keys_from_db())

        self.assertListEqual(
            sorted(response), ["image-1.jpg", "image-2.jpg", "image-3.jpg"]
        )


class TestDeleteUnusedFiles(TestCase):
    def setUp(self):
        create_db_tables_sync(Movie, Director, Studio)

    def tearDown(self):
        drop_db_tables_sync(Movie, Director, Studio)

    def test_get_file_keys_from_db(self):
        media_path = os.path.join(
            tempfile.gettempdir(), "piccolo-admin-test-unused-files"
        )

        if os.path.exists(media_path):
            shutil.rmtree(media_path)

        os.mkdir(media_path)

        file_names = ["image-1.jpg", "image-2.jpg", "image-3.jpg"]
        extra_file_name = "image-4.jpg"

        Movie.insert(
            *[Movie(poster=file_name) for file_name in file_names]
        ).run_sync()

        for file_name in [*file_names, extra_file_name]:
            with open(os.path.join(media_path, file_name), "wb") as _:
                pass

        storage = LocalMediaStorage(column=Movie.poster, media_path=media_path)

        asyncio.run(storage.delete_unused_files(auto=True))

        # The extra_file_name should have been deleted.
        self.assertListEqual(sorted(os.listdir(media_path)), file_names)


class TestHash(TestCase):
    """
    We want to be able to detect if multiple storage classes are
    accidentally referencing the same folder.
    """

    def test_local_media(self):
        """
        Test comparing ``LocalMediaStorage``.
        """
        # These should be equal, as the media path is the same.
        self.assertEqual(
            LocalMediaStorage(column=Movie.poster, media_path="/tmp/"),
            LocalMediaStorage(column=Movie.screenshots, media_path="/tmp/"),
        )

        # These shouldn't be equal, as the media paths are different.
        self.assertNotEqual(
            LocalMediaStorage(column=Movie.poster, media_path="/tmp/poster/"),
            LocalMediaStorage(
                column=Movie.screenshots, media_path="/tmp/screenshots/"
            ),
        )

    def test_s3_media(self):
        """
        Test comparing ``S3MediaStorage``.
        """
        # These should be equal, as the folder name and bucket name as the
        # same.
        self.assertEqual(
            S3MediaStorage(
                column=Movie.poster,
                bucket_name="bucker123",
                folder_name="folder123",
            ),
            S3MediaStorage(
                column=Movie.screenshots,
                bucket_name="bucker123",
                folder_name="folder123",
            ),
        )

        # These shouldn't be equal, as the folder names are different.
        self.assertNotEqual(
            S3MediaStorage(
                column=Movie.poster,
                bucket_name="bucker123",
                folder_name="folder123",
            ),
            S3MediaStorage(
                column=Movie.screenshots,
                bucket_name="bucker123",
                folder_name="folder456",
            ),
        )

        # These shouldn't be equal, as the bucket names are different.
        self.assertNotEqual(
            S3MediaStorage(
                column=Movie.poster,
                bucket_name="bucker123",
                folder_name="folder123",
            ),
            S3MediaStorage(
                column=Movie.screenshots,
                bucket_name="bucker456",
                folder_name="folder123",
            ),
        )

        # These shouldn't be equal, as the endpoint URLs are different.
        self.assertNotEqual(
            S3MediaStorage(
                column=Movie.poster,
                connection_kwargs={"endpoint_url": "https://cloud-1.com"},
                bucket_name="bucker123",
                folder_name="folder123",
            ),
            S3MediaStorage(
                column=Movie.screenshots,
                connection_kwargs={"endpoint_url": "https://cloud-2.com"},
                bucket_name="bucker123",
                folder_name="folder123",
            ),
        )

    def test_mix(self):
        """
        Test comparing a mix of ``LocalMediaStorage`` and ``S3MediaStorage``.
        """
        self.assertNotEqual(
            LocalMediaStorage(column=Movie.poster, media_path="/tmp/"),
            S3MediaStorage(
                column=Movie.screenshots,
                bucket_name="bucker123",
                folder_name="folder456",
            ),
        )

    def test_sets(self):
        """
        Make sure sets behave as expected.
        """
        self.assertEqual(
            len(
                {
                    LocalMediaStorage(column=Movie.poster, media_path="/tmp/"),
                    LocalMediaStorage(
                        column=Movie.screenshots, media_path="/tmp/"
                    ),
                },
            ),
            1,
        )
