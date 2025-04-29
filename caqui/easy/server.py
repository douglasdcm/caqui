from time import sleep
from typing import Union
from requests import head
from requests.exceptions import ConnectionError
import requests
import subprocess
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.chrome import ChromeDriverManager
from caqui.exceptions import ServerError


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
        self.__browser = browser
        self.__port = port
        self.__process = None

    def __browser_factory(self):
        if not self.__browser:
            driver_manager = ChromeDriverManager().install()
        else:
            driver_manager = self.__browser.install()
        return driver_manager

    def __wait_server(self):
        MAX_RETIES = 10
        for i in range(MAX_RETIES):
            try:
                requests.get(self.url)
                break
            except ConnectionError:
                sleep(1)
                if i == (MAX_RETIES - 1):
                    self.__process.kill()
                    self.__process.wait()
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
            head(self.url)
        except ConnectionError:
            pass
        except Exception:
            raise

        driver_manager = self.__browser_factory()
        self.__process = subprocess.Popen(
            [driver_manager, f"--port={self.__port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        if self.__process is None:
            raise ServerError("Not able to start the server.")

        self.__wait_server()

    @property
    def url(self):
        """
        Returns the driver URL.
        """
        return f"http://localhost:{self.__port}"

    @property
    def process(self):
        """Returns the process (PID)"""
        return self.__process

    def dispose(self):
        """
        Disposes the driver process.
        """
        if self.__process:
            self.__process.kill()
            self.__process.wait()
            self.__process = None
