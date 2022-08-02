import os
import uuid
from unittest import TestCase
from unittest.mock import MagicMock, patch

import boto3
from moto import mock_s3

from piccolo_admin.example import Movie
from piccolo_admin.media.s3 import S3MediaStorage


class TestS3MediaStorage(TestCase):
    @patch("piccolo_admin.media.base.uuid")
    @patch("piccolo_admin.media.s3.S3MediaStorage.get_client")
    def test_store_file(self, get_client: MagicMock, uuid_module: MagicMock):
        """
        Make sure we can store files, and retrieve them.
        """
        uuid_module.uuid4.return_value = uuid.UUID(
            "fd0125c7-8777-4976-83c1-81605d5ab155"
        )

        with mock_s3():
            s3 = boto3.resource("s3", region_name="us-east-1")
            s3.create_bucket(Bucket="posters")

            connection_kwargs = {
                "aws_access_key_id": "abc123",
                "aws_secret_access_key": "xyz123",
                "region_name": "us-east-1",
            }

            get_client.return_value = boto3.client("s3", **connection_kwargs)

            storage = S3MediaStorage(
                column=Movie.poster,
                bucket_name="posters",
                connection_kwargs=connection_kwargs,
            )

            with open(
                os.path.join(os.path.dirname(__file__), "test_files/bulb.jpg"),
                "rb",
            ) as test_file:
                # Store the file
                file_id = storage.store_file_sync(
                    file_name="bulb.jpg", file=test_file
                )

                # Retrieve the URL for the file
                url = storage.generate_file_url_sync(file_id, root_url="")

                path, params = url.split("?", 1)

                self.assertEqual(
                    path, f"https://posters.s3.amazonaws.com/{file_id}"
                )

                # We're parsing a string like this:
                # AWSAccessKeyId=abc123&Signature=abc123&Expires=1659437428
                params_list = [i.split("=") for i in params.split("&")]

                params_dict = {i[0]: i[1] for i in params_list}

                self.assertEqual(
                    params_dict["AWSAccessKeyId"],
                    connection_kwargs["aws_access_key_id"],
                )
                self.assertTrue("Signature" in params_dict)
                self.assertTrue("Expires" in params_dict)
