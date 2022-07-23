import abc
import typing as t


class MediaHandler(abc.ABC):
    """
    If you want to implement media uploads, use a subclass of this class.
    """

    @abc.abstractmethod
    def store_file(self, file: t.IO) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_file(self, file_id: str):
        raise NotImplementedError


class LocalMediaHandler(MediaHandler):
    def __init__(self, root_path: str):
        """
        Stores media files on a local path. This is good for simple
        applications, where you're happy with the media files being stored
        on a single server.

        :param root_path:
            This is the local folder where the media files will be stored. It
            should be an absolute path. For example, ``/srv/piccolo-media/``.

        """
        self.root_path = root_path

    def store_file(self, file: t.IO) -> str:
        ...

    def retrieve_file(self, file_id: str):
        ...
