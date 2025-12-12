# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import subprocess
from time import sleep
from typing import Dict, Optional

import requests
from requests import head
from requests.exceptions import ConnectionError
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

from caqui.exceptions import ServerError, WebDriverError

TIMEOUT: int = 120  # seconds

CHROME: str = "chrome"
FIREFOX: str = "firefox"
EDGE: str = "edge"
OPERA: str = "opera"
DRIVER_MANAGER: Dict[str, type] = {
    CHROME: ChromeDriverManager,
    FIREFOX: GeckoDriverManager,
    EDGE: EdgeChromiumDriverManager,
    OPERA: OperaDriverManager,
}


class LocalServer:
    """
    Starts and stops the local server. Cannot be used with remote servers

    Args:
        browser: if is `None`, then a simple `ChromeDriverManager` is used
        Reference: https://pypi.org/project/webdriver-manager/#use-with-chrome

        port: the port to start the local server
        executable_path: the path where the driver. For example:
        /home/my-user/.wdm/drivers/geckodriver/linux64/v0.36.0/geckodriver
        /home/my-user/.wdm/drivers/operadriver/linux64/v.140.0.7339.249/operadriver_linux64/operadriver
        /home/my-user/.wdm/drivers/chromedriver/linux64/142.0.7444.175/chromedriver-linux64
    """

    def __init__(self, port: int = 9999, executable_path: Optional[str] = None) -> None:
        self._browser: Optional[str] = None
        self._port: int = port
        self._process: Optional[subprocess.Popen] = None
        self._executable_path: Optional[str] = executable_path

    def _browser_factory(self) -> str:
        browser: Optional[type] = DRIVER_MANAGER.get(self._browser)  # type: ignore
        if self._executable_path:
            return self._executable_path
        if browser:
            return browser().install()
        raise WebDriverError(f"Browser {self._browser} not supported")

    def _wait_server(self) -> None:
        MAX_RETIES: int = 10
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

    def start(self) -> None:
        """Starts the local server when the `executable_path` is provided"""
        try:
            head(self.url, timeout=TIMEOUT)
        except ConnectionError:
            pass
        except Exception:
            raise

        driver_manager: str = self._browser_factory()
        self._process = subprocess.Popen(
            [driver_manager, f"--port={self._port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        if self._process is None:
            raise ServerError("Not able to start the server.")

        self._wait_server()

    @property
    def url(self) -> str:
        """
        Returns the driver URL.
        """
        return f"http://localhost:{self._port}"

    @property
    def process(self) -> Optional[subprocess.Popen]:
        """Returns the process (PID)"""
        return self._process

    def start_chrome(self) -> None:
        """
        Start a Chrome browser instance for the server.

        Sets the browser type to CHROME and initializes the server startup process.
        """
        self._browser = CHROME
        self.start()

    def start_firefox(self) -> None:
        """
        Start Firefox browser for the current session.

        Sets the browser type to Firefox and initiates the browser startup process.

        Returns:
            None
        """
        self._browser = FIREFOX
        self.start()

    def start_opera(self) -> None:
        """
        Initialize and start the Opera browser instance.

        Sets the browser type to Opera and initiates the browser startup process.
        """
        self._browser = OPERA
        self.start()

    def start_edge(self) -> None:
        """
        Start the Edge browser and initialize the server.

        This method sets the internal browser instance to EDGE and calls the start method
        to initialize the server with the Edge browser.

        Returns:
            None
        """
        self._browser = EDGE
        self.start()

    def dispose(self, delay: float = 0) -> None:
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
