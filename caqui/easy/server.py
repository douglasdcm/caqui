# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import requests
import subprocess
from time import sleep
from typing import Union
from requests import head
from requests.exceptions import ConnectionError
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.chrome import ChromeDriverManager
from caqui.exceptions import ServerError


TIMEOUT = 120  # seconds


class Server:
    """
    Starts and stops the local server. Cannot be used with remote servers

    Args:
        browser: if is `None`, then a simple `ChromeDriverManager` is used
        Reference: https://pypi.org/project/webdriver-manager/#use-with-chrome

        port: the port to start the local server
    """

    _instance = None

    def __init__(self, browser: Union[DriverManager, None] = None, port=9999):
        self._browser = browser
        self._port = port
        self._sprocess = None

    def _browser_factory(self):
        if not self._browser:
            driver_manager = ChromeDriverManager().install()
        else:
            driver_manager = self._browser.install()
        return driver_manager

    def _wait_server(self):
        MAX_RETIES = 10
        for i in range(MAX_RETIES):
            try:
                requests.get(self.url, timeout=TIMEOUT)
                break
            except ConnectionError:
                sleep(0.5)
                if i == (MAX_RETIES - 1) and self._process:
                    self._process.kill()
                    self._process.wait()
                    raise Exception("Driver not started")

    @staticmethod
    def get_instance(browser: Union[DriverManager, None] = None, port=9999):
        """(Singleton) Returns the current instance of the server"""
        if Server._instance is None:
            Server._instance = Server(browser, port)
        return Server._instance

    def start(self):
        """Starts the local server"""
        try:
            head(self.url, timeout=TIMEOUT)
        except ConnectionError:
            pass
        except Exception:
            raise

        driver_manager = self._browser_factory()
        self._process: Union[subprocess.Popen, None] = subprocess.Popen(
            [driver_manager, f"--port={self._port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        if self._process is None:
            raise ServerError("Not able to start the server.")

        self._wait_server()

    @property
    def url(self):
        """
        Returns the driver URL.
        """
        return f"http://localhost:{self._port}"

    @property
    def process(self):
        """Returns the process (PID)"""
        return self._process

    def dispose(self, delay: float = 0):
        """
        Disposes the driver process.

        Args:
            delay: Delay execution for a given number of seconds.
            The argument may be a floating point number for subsecond precision.
        """
        if delay:
            sleep(delay)
        if self._process:
            self._process.kill()
            self._process.wait()
            self._process = None
