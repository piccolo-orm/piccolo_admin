from __future__ import annotations

import abc
import asyncio
import os
import pathlib
import shutil
import typing as t
import uuid
from concurrent.futures import ThreadPoolExecutor

from piccolo.apps.user.tables import BaseUser
from piccolo.utils.sync import run_sync

if t.TYPE_CHECKING:
    from concurrent.futures._base import Executor


# TODO - might move this to Piccolo API.
class MediaStorage(metaclass=abc.ABCMeta):
    """
    If you want to implement media uploads, use a subclass of this class.
    """

    def generate_file_id(
        self, file_name: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        Generates a unique file ID. If you have your own strategy for naming
        files, you can override this method.

        By default we add a UUID to the filename, to make it unique::

            >>> self.generate_file_id(file_name='my-poster.jpg')
            my-poster-3beac950-7721-46c9-9e7d-5e908ef51011.jpg

        :raises ValueError:
            If the ``file_name`` is invalid.

        """
        # Don't allow the file to begin with a dot, otherwise it will be a
        # hidden file on Unix.
        if file_name.startswith("."):
            raise ValueError("File names must not start with a period.")

        if not file_name:
            # It's unlikely that the file_name is an empty string, but just in
            # case.
            raise ValueError("The file has no name.")

        uuid_ = uuid.uuid4()

        components = file_name.rsplit(".", 1)
        if len(components) == 2:
            name, extension = components

            if len(extension) > 10:
                # We could check whether the file extension is a recognised
                # one, but it's hard to have a definitive list of valid
                # extensions.
                raise ValueError("Suspiciously long file extension.")

        else:
            name = file_name
            extension = None

        if len(file_name) > 50:
            # Truncate really long names. Otherwise they might be too long
            # for some operating systems, or too long to be stored in a
            # database field.
            name = file_name[:50]

        file_id = f"{name}-{uuid_}"
        if extension:
            file_id += f".{extension}"

        return file_id

    @abc.abstractmethod
    async def store_file(
        self, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        Stores the file in whichever storage you're using, and returns a key
        which uniquely identifes the file.

        :param file:
            The file to store.
        :param user:
            The Piccolo ``BaseUser`` who requested this.

        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file_url(
        self, file_id: str, user: t.Optional[BaseUser] = None
    ):
        """
        This retrieves an absolute URL for the file. It might be a signed URL,
        if using S3 for storage.

        :param file_id:
            Get the URL for a file with this file_id.
        :param user:
            The Piccolo ``BaseUser`` who requested this.
        """
        raise NotImplementedError


class LocalMediaStorage(MediaStorage):
    def __init__(
        self,
        media_path: str,
        media_url: str,
        executor: t.Optional[Executor] = None,
    ):
        """
        Stores media files on a local path. This is good for simple
        applications, where you're happy with the media files being stored
        on a single server.

        :param media_path:
            This is the local folder where the media files will be stored. It
            should be an absolute path. For example, ``'/srv/piccolo-media/'``.
        :param media_url:
            This is the URL where media is served from. For example:
            ``'/media/'``.
        :param executor:
            An executor, which file save operations are run in, to avoid
            blocking the event loop.
        """
        self.media_path = media_path
        self.media_url = media_url
        self.exector = executor or ThreadPoolExecutor(max_workers=10)

    async def store_file(
        self, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        # file.name includes the entire path (e.g. /foo/bar.jpg) - we just want
        # bar.jpg.
        file_name = pathlib.Path(file.name).name

        file_id = self.generate_file_id(file_name=file_name, user=user)

        loop = asyncio.get_running_loop()

        def save():
            with open(
                os.path.join(self.media_path, file_id), "wb"
            ) as new_file:
                shutil.copyfileobj(file, new_file)

        await loop.run_in_executor(self.exector, save)

        return file_id

    def store_file_sync(
        self, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`store_file`.
        """
        return run_sync(self.store_file(file=file, user=user))

    async def get_file_url(
        self, file_id: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        This retrieves an absolute URL for the file.
        """
        return "/".join((self.media_url.rstrip("/"), file_id))

    def get_file_url_sync(
        self, file_id: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`get_file_url`.
        """
        return run_sync(self.get_file_url(file_id=file_id, user=user))
