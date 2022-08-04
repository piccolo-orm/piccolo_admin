from __future__ import annotations

import asyncio
import functools
import pathlib
import sys
import typing as t
from concurrent.futures import ThreadPoolExecutor

from piccolo.apps.user.tables import BaseUser
from piccolo.columns.column_types import Array, Text, Varchar

from .base import ALLOWED_CHARACTERS, ALLOWED_EXTENSIONS, MediaStorage

if t.TYPE_CHECKING:  # pragma: no cover
    from concurrent.futures._base import Executor


class S3MediaStorage(MediaStorage):
    def __init__(
        self,
        column: t.Union[Text, Varchar, Array],
        bucket_name: str,
        folder_name: str,
        connection_kwargs: t.Dict[str, t.Any] = None,
        signed_url_expiry: int = 3600,
        executor: t.Optional[Executor] = None,
        allowed_extensions: t.Optional[t.Sequence[str]] = ALLOWED_EXTENSIONS,
        allowed_characters: t.Optional[t.Sequence[str]] = ALLOWED_CHARACTERS,
    ):
        """
        Stores media files in S3 compatible storage. This is a good option when
        you have lots of files to store, and don't want them stored locally
        on a server. Many cloud providers provide S3 compatible storage,
        besides from Amazon Web Services.

        :param column:
            The Piccolo ``Column`` which the storage is for.
        :param bucket_name:
            Which S3 bucket the files are stored in.
        :param folder:
            The files will be stored in this folder within the bucket. S3
            buckets don't really have folders, but if ``folder`` is
            ``'movie_screenshots'``, then we store the file at
            ``'movie_screenshots/my-file-abc-123.jpeg'``, to simulate it being
            in a folder.
        :param connection_kwargs:
            These kwargs are passed directly to ``boto3``. Learn more about
            `available options <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client>`_.
            For example::

                S3MediaStorage(
                    ...,
                    connection_kwargs={
                        'aws_access_key_id': 'abc123',
                        'aws_secret_access_key': 'xyz789',
                        'endpoint_url': 's3.cloudprovider.com',
                        'region_name': 'uk'
                    }
                )

        :param signed_url_expiry:
            Files are accessed via signed URLs, which are only valid for this
            number of seconds.
        :param executor:
            An executor, which file save operations are run in, to avoid
            blocking the event loop. If not specified, we use a sensibly
            configured :class:`ThreadPoolExecutor <concurrent.futures.ThreadPoolExecutor>`.
        :param allowed_extensions:
            Which file extensions are allowed. If ``None``, then all extensions
            are allowed (not recommended unless the users are trusted).
        :param allowed_characters:
            Which characters are allowed in the file name. By default, it's
            very strict. If set to ``None`` then all characters are allowed.
        """  # noqa: E501

        try:
            import boto3  # noqa
        except ImportError:  # pragma: no cover
            sys.exit(
                "Please install boto3 to use this feature "
                "`pip install 'piccolo_admin[s3]'`"
            )
        else:
            self.boto3 = boto3

        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.connection_kwargs = connection_kwargs
        self.signed_url_expiry = signed_url_expiry
        self.executor = executor or ThreadPoolExecutor(max_workers=10)

        super().__init__(
            column=column,
            allowed_extensions=allowed_extensions,
            allowed_characters=allowed_characters,
        )

    def get_client(self):  # pragma: no cover
        """
        Returns an S3 clent.
        """
        session = self.boto3.session.Session()
        client = session.client(
            "s3",
            **self.connection_kwargs,
        )
        return client

    async def store_file(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        loop = asyncio.get_running_loop()

        blocking_function = functools.partial(
            self.store_file_sync, file_name=file_name, file=file, user=user
        )

        file_key = await loop.run_in_executor(self.executor, blocking_function)

        return file_key

    def store_file_sync(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`store_file`.
        """
        file_key = self.generate_file_key(file_name=file_name, user=user)

        client = self.get_client()

        client.upload_fileobj(
            file,
            self.bucket_name,
            str(pathlib.Path(self.folder_name, file_key)),
        )

        return file_key

    async def generate_file_url(
        self, file_key: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        This retrieves an absolute URL for the file.
        """
        loop = asyncio.get_running_loop()

        blocking_function: t.Callable = functools.partial(
            self.generate_file_url_sync,
            file_key=file_key,
            root_url=root_url,
            user=user,
        )

        return await loop.run_in_executor(self.executor, blocking_function)

    def generate_file_url_sync(
        self, file_key: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`generate_file_url`.
        """
        s3_client = self.get_client()

        return s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": str(pathlib.Path(self.folder_name, file_key)),
            },
            ExpiresIn=self.signed_url_expiry,
        )

    ###########################################################################

    async def get_file(self, file_key: str) -> t.Optional[t.IO]:
        """
        Returns the file object matching the ``file_key``.
        """
        loop = asyncio.get_running_loop()

        func = functools.partial(self.get_file_sync, file_key=file_key)

        return await loop.run_in_executor(self.executor, func)

    def get_file_sync(self, file_key: str) -> t.Optional[t.IO]:
        """
        Returns the file object matching the ``file_key``.
        """
        s3_client = self.get_client()
        response = s3_client.get_object(
            Bucket=self.bucket_name,
            Key=str(pathlib.Path(self.folder_name, file_key)),
        )
        return response["Body"]

    async def delete_file(self, file_key: str):
        """
        Deletes the file object matching the ``file_key``.
        """
        loop = asyncio.get_running_loop()

        func = functools.partial(
            self.delete_file_sync,
            file_key=file_key,
        )

        return await loop.run_in_executor(self.executor, func)

    def delete_file_sync(self, file_key: str):
        """
        Deletes the file object matching the ``file_key``.
        """
        s3_client = self.get_client()
        return s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=str(pathlib.Path(self.folder_name, file_key)),
        )

    async def bulk_delete_files(self, file_keys: t.List[str]):
        loop = asyncio.get_running_loop()
        func = functools.partial(
            self.bulk_delete_files_sync,
            file_keys=file_keys,
        )
        await loop.run_in_executor(self.executor, func)

    def bulk_delete_files_sync(self, file_keys: t.List[str]):
        s3_client = self.get_client()

        batch_size = 100
        iteration = 0
        folder_name = self.folder_name

        while True:
            batch = file_keys[
                (iteration * batch_size) : (  # noqa: E203
                    iteration + 1 * batch_size
                )
            ]
            if not batch:
                # https://github.com/nedbat/coveragepy/issues/772
                break  # pragma: no cover

            s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    "Objects": [
                        {"Key": str(pathlib.Path(folder_name, file_key))}
                        for file_key in file_keys
                    ],
                },
            )

            iteration += 1

    def get_file_keys_sync(self) -> t.List[str]:
        """
        Returns the file key for each file we have stored.
        """
        s3_client = self.get_client()

        keys = []
        start_after = None

        while True:
            extra_kwargs: t.Dict[str, t.Any] = (
                {"StartAfter": start_after} if start_after else {}
            )

            response = s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=self.folder_name,
                **extra_kwargs,
            )

            contents = response.get("Contents")

            if contents:
                for obj in contents:
                    keys.append(obj["Key"])

                start_after = keys[-1]
            else:
                # https://github.com/nedbat/coveragepy/issues/772
                break  # pragma: no cover

        prefix = f"{self.folder_name}/"

        return [i.lstrip(prefix) for i in keys]

    async def get_file_keys(self) -> t.List[str]:
        """
        Returns the file key for each file we have stored.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor, self.get_file_keys_sync
        )

    def __hash__(self):
        return hash(
            (
                "s3",
                self.connection_kwargs.get("endpoint_url")
                if self.connection_kwargs
                else None,
                self.bucket_name,
                self.folder_name,
            )
        )

    def __eq__(self, value):
        if not isinstance(value, S3MediaStorage):
            return False
        return value.__hash__() == self.__hash__()
