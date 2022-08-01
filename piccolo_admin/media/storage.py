"""
Resources:
https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
"""

from __future__ import annotations

import abc
import asyncio
import os
import pathlib
import shutil
import string
import typing as t
import uuid
from concurrent.futures import ThreadPoolExecutor

from piccolo.apps.user.tables import BaseUser
from piccolo.utils.sync import run_sync

if t.TYPE_CHECKING:
    from concurrent.futures._base import Executor


logger = logging.getLogger(__file__)


AUDIO_EXTENSIONS = (
    "mp3",
    "wav",
)

DATA_EXTENSIONS = (
    "csv",
    "tsv",
)

DOCUMENT_EXTENSIONS = ("pdf",)

IMAGE_EXTENSIONS = (
    "gif",
    "jpeg",
    "jpg",
    "png",
    "svg",
    "tif",
    "webp",
)

TEXT_EXTENSIONS = (
    "rtf",
    "txt",
)

VIDEO_EXTENSIONS = ("mov", "mp4", "webm")

ALLOWED_EXTENSIONS = (
    *AUDIO_EXTENSIONS,
    *DATA_EXTENSIONS,
    *DOCUMENT_EXTENSIONS,
    *IMAGE_EXTENSIONS,
    *TEXT_EXTENSIONS,
    *VIDEO_EXTENSIONS,
)

ALLOWED_CHARACTERS = (
    *string.ascii_letters,
    *string.digits,
    " ",
    "-",
    "_",
    ".",
)


# TODO - might move this to Piccolo API.
class MediaStorage(metaclass=abc.ABCMeta):
    """
    If you want to implement media uploads, use a subclass of this class.
    """

    def __init__(
        self,
        allowed_extensions: t.Optional[t.Sequence[str]] = ALLOWED_EXTENSIONS,
        allowed_characters: t.Optional[t.Sequence[str]] = ALLOWED_CHARACTERS,
    ):
        self.allowed_extensions = (
            [i.lower() for i in allowed_extensions]
            if allowed_extensions
            else None
        )
        self.allowed_characters = allowed_characters

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
        if not file_name:
            # It's unlikely that the file_name is an empty string, but just in
            # case.
            raise ValueError("The file name can't be empty.")

        # If the file_name includes the entire path (e.g. /foo/bar.jpg) - we
        # just want bar.jpg.
        file_name = pathlib.Path(file_name).name

        # Don't allow the file name to begin with a dot, otherwise it will be a
        # hidden file on Unix.
        if file_name.startswith("."):
            raise ValueError("File names must not start with a period.")

        # Don't allow double dots in the file name, in case it allows a file to
        # be written to a parent folder.
        if ".." in file_name:
            raise ValueError("File names must not contain '..'.")

        if self.allowed_characters:
            # Having some restriction on the allowed characters is important,
            # in case there are things like null bytes in there.
            # https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html#extension-validation
            for character in file_name:
                if character not in self.allowed_characters:
                    raise ValueError(
                        f"'{character}' is not allowed in the filename."
                    )

        components = file_name.rsplit(".", 1)

        if len(components) == 2:
            name, extension = components

            if self.allowed_extensions:
                if extension.lower() not in self.allowed_extensions:
                    # TODO - inspect the files to make sure they are what
                    # they say they are.
                    raise ValueError("This file type isn't allowed.")
        else:
            raise ValueError("The file has no extension.")

        if len(file_name) > 50:
            # Truncate really long names. Otherwise they might be too long
            # for some operating systems, or too long to be stored in a
            # database field.
            name = name[:50]

        uuid_ = uuid.uuid4()

        file_id = f"{name}-{uuid_}"
        if extension:
            file_id += f".{extension}"

        return file_id

    @abc.abstractmethod
    async def store_file(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
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
    async def generate_file_url(
        self, file_id: str, root_url: str, user: t.Optional[BaseUser] = None
    ):
        """
        This retrieves an absolute URL for the file. It might be a signed URL,
        if using S3 for storage.

        :param file_id:
            Get the URL for a file with this file_id.
        :param root_url:
            The URL the media is usually served from. The sub class might
            ignore this argument entirely, if it's fetching the data from
            an external source like S3.
        :param user:
            The Piccolo ``BaseUser`` who requested this.
        """
        raise NotImplementedError


class LocalMediaStorage(MediaStorage):
    def __init__(
        self,
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

        :param media_path:
            This is the local folder where the media files will be stored. It
            should be an absolute path. For example, ``'/srv/piccolo-media/'``.
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
            allowed_extensions=allowed_extensions,
            allowed_characters=allowed_characters,
        )

    async def store_file(
        self, file_name: str, file: t.IO, user: t.Optional[BaseUser] = None
    ) -> str:
        # If the file_name includes the entire path (e.g. /foo/bar.jpg) - we
        # just want bar.jpg.
        file_name = pathlib.Path(file_name).name

        file_id = self.generate_file_id(file_name=file_name, user=user)

        loop = asyncio.get_running_loop()
        file_permissions = self.file_permissions

        def save():
            path = os.path.join(self.media_path, file_id)

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

        return file_id

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
        self, file_id: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        This retrieves an absolute URL for the file.
        """
        return "/".join((root_url.rstrip("/"), file_id))

    def generate_file_url_sync(
        self, file_id: str, root_url: str, user: t.Optional[BaseUser] = None
    ) -> str:
        """
        A sync wrapper around :meth:`generate_file_url`.
        """
        return run_sync(
            self.generate_file_url(
                file_id=file_id, root_url=root_url, user=user
            )
        )
