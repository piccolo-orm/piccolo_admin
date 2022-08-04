from __future__ import annotations

import asyncio
import functools
import logging
import os
import pathlib
import shutil
import typing as t
from concurrent.futures import ThreadPoolExecutor

from piccolo.apps.user.tables import BaseUser
from piccolo.columns.column_types import Array, Text, Varchar
from piccolo.utils.sync import run_sync

from .base import ALLOWED_CHARACTERS, ALLOWED_EXTENSIONS, MediaStorage

if t.TYPE_CHECKING:  # pragma: no cover
    from concurrent.futures._base import Executor


logger = logging.getLogger(__file__)


class LocalMediaStorage(MediaStorage):
    def __init__(
        self,
        column: t.Union[Text, Varchar, Array],
        media_path: str,
        executor: t.Optional[Executor] = None,
        allowed_extensions: t.Optional[t.Sequence[str]] = ALLOWED_EXTENSIONS,
        allowed_characters: t.Optional[t.Sequence[str]] = ALLOWED_CHARACTERS,
        file_permissions: t.Optional[int] = 0o640,
    ):
        """
        Stores media files on a local path. This is good for simple
        applications, where you're happy with the media files being stored
        on a single server.

        :param column:
            The Piccolo ``Column`` which the storage is for.
        :param media_path:
            This is the local folder where the media files will be stored. It
            should be an absolute path. For example,
            ``'/srv/piccolo-media/poster/'``.
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
        :param file_permissions:
            If set to a value other than ``None``, then all uploaded files are
            given these file permissions.
        """  # noqa: E501
        self.media_path = media_path
        self.executor = executor or ThreadPoolExecutor(max_workers=10)
        self.file_permissions = file_permissions

        if not os.path.exists(media_path):
            os.mkdir(self.media_path)

        super().__init__(
            column=column,
            allowed_extensions=allowed_extensions,
            allowed_characters=allowed_characters,
        )

    async def store_file(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        # If the file_name includes the entire path (e.g. /foo/bar.jpg) - we
        # just want bar.jpg.
        file_name = pathlib.Path(file_name).name

        file_key = self.generate_file_key(file_name=file_name, user=user)

        loop = asyncio.get_running_loop()
        file_permissions = self.file_permissions

        def save():
            path = os.path.join(self.media_path, file_key)

            if os.path.exists(path):
                logger.error(
                    "A file name clash has occurred - the chances are very "
                    "low. Could be malicious, or a serious bug."
                )
                raise IOError("Unable to save the file")

            with open(path, "wb") as new_file:
                shutil.copyfileobj(file, new_file)
                if file_permissions is not None:
                    os.chmod(path, 0o640)

        await loop.run_in_executor(self.executor, save)

        return file_key

    def store_file_sync(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`store_file`.
        """
        return run_sync(
            self.store_file(file_name=file_name, file=file, user=user)
        )

    async def generate_file_url(
        self, file_key: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        This retrieves an absolute URL for the file.
        """
        return "/".join((root_url.rstrip("/"), file_key))

    def generate_file_url_sync(
        self, file_key: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`generate_file_url`.
        """
        return run_sync(
            self.generate_file_url(
                file_key=file_key, root_url=root_url, user=user
            )
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
        A sync wrapper around :meth:`get_file`.
        """
        path = os.path.join(self.media_path, file_key)
        return open(path, "rb")

    async def delete_file(self, file_key: str):
        """
        Deletes the file object matching the ``file_key``.
        """
        loop = asyncio.get_running_loop()
        func = functools.partial(self.delete_file_sync, file_key=file_key)
        return await loop.run_in_executor(self.executor, func)

    def delete_file_sync(self, file_key: str):
        """
        A sync wrapper around :meth:`delete_file`.
        """
        path = os.path.join(self.media_path, file_key)
        os.unlink(path)

    async def bulk_delete_files(self, file_keys: t.List[str]):
        media_path = self.media_path
        for file_key in file_keys:
            os.unlink(os.path.join(media_path, file_key))

    async def get_file_keys(self) -> t.List[str]:
        """
        Returns the file key for each file we have stored.
        """
        file_keys = []
        for (_, _, filenames) in os.walk(self.media_path):
            file_keys.extend(filenames)
            break

        return file_keys

    def __hash__(self):
        return hash(("local", self.media_path))

    def __eq__(self, value):
        if not isinstance(value, LocalMediaStorage):
            return False
        return value.__hash__() == self.__hash__()
