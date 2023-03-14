import time
from http.client import HTTPConnection
from subprocess import PIPE, Popen

import pytest

from piccolo_admin.example import set_engine

HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"
USERNAME = "piccolo"
PASSWORD = "piccolo123"


@pytest.fixture(scope="session", autouse=True)
def set_db_engine():
    set_engine()


@pytest.fixture
def browser_context_args():
    return {"record_video_dir": "videos/"}


@pytest.fixture
def dev_server():
    """
    Running dev server and Playwright test in parallel.
    More info https://til.simonwillison.net/pytest/playwright-pytest
    """
    process = Popen(
        ["python", "-m", "piccolo_admin.example"],
        stdout=PIPE,
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection(f"{HOST}:{PORT}")
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield process
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1

    if not retries:
        raise RuntimeError("Failed to start http server")
    else:
        process.terminate()
        process.wait()
