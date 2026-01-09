import json
import subprocess
import time
import urllib.request

import requests

from caqui.constants import TIMEOUT
from caqui.exceptions import ServerError

WS_URL = "http://127.0.0.1"
PORT = 9222


class LocalServerCDP:
    def __init__(self, port=PORT):
        self._port = port
        self._process = None

    @property
    def port(self):
        return self._port

    @property
    def ws_url(self):
        return self.get_ws_url()

    def start_chrome(self):
        self._start_browser("google-chrome")

    def start_opera(self):
        self._start_browser("opera")


    def start_edge(self):
        return self._start_browser("microsoft-edge")

    def _start_browser(self, browser):
        self._process = subprocess.Popen(
            [
                browser,
                f"--remote-debugging-port={self._port}",
                f"--user-data-dir=/tmp/cdp-profile-{self._port}",
                "--no-first-run",
                "--no-default-browser-check",
                "--headless",
                "--no-zygote",
                "--no-sandbox",
                "about:blank",
                f"--remote-allow-origins={WS_URL}:{self._port}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        if self._process is None:
            raise ServerError("Not able to start the server.")
        self._wait_server()

    def _wait_server(self) -> None:
        MAX_RETIES: int = 10
        for i in range(MAX_RETIES):
            try:
                requests.get(f"{WS_URL}:{self._port}", timeout=TIMEOUT)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
                if i == (MAX_RETIES - 1) and self._process:
                    self._process.kill()
                    self._process.wait()
                    raise Exception("Driver not started")

    def dispose(self, delay=0):
        if delay:
            time.sleep(delay)
        if self._process:
            self._process.kill()
            self._process.wait()
            self._process = None

    def get_ws_url(self):
        return get_ws_url(self._port)


def get_ws_url(port=PORT):
    with urllib.request.urlopen(f"{WS_URL}:{port}/json") as r:
        targets = json.loads(r.read())
        return targets[0]["webSocketDebuggerUrl"]
