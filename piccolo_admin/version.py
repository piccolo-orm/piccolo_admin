import os


def get_version():
    with open(os.path.join(os.path.dirname(__file__), "version.txt")) as f:
        return f.read().strip()


__VERSION__ = get_version()
