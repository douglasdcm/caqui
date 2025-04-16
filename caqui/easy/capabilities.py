import json
import math
import time
from typing import Union
import requests
import subprocess
from requests.exceptions import ConnectionError
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.chrome import ChromeDriverManager
from caqui.exceptions import CapabilityNotSupported


class Browser:
    """
    https://pypi.org/project/webdriver-manager/
    """

    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    OPERA = "opera"
    IE = "internet explorer"


class ProxyConfigurationBuilder:
    """
    Reference: https://www.w3.org/TR/webdriver/#dfn-proxy-configuration
    """

    def __init__(self) -> None:
        self.__proxy = {}

    def proxy_type(self, proxy: str):
        """
        Indicates the type of proxy configuration.

        proxy: pac, direct, autodetect, system, or manual.

        Reference: https://www.w3.org/TR/webdriver/#dfn-proxy-configuration
        """
        self.__proxy = {
            **self.__proxy,
            "proxyType": proxy,
        }
        return self

    def proxy_autoconfig_url(self, url: str):
        """
        Defines the URL for a proxy auto-config file if proxyType is equal to "pac".
        """
        self.__proxy = {
            **self.__proxy,
            "proxyAutoconfigUrl": url,
        }
        return self

    def ftp_proxy(self, proxy: str):
        """
        Defines the proxy host for FTP traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "ftp".
        """
        self.__proxy = {
            **self.__proxy,
            "ftpProxy": proxy,
        }
        return self

    def http_proxy(self, proxy: str):
        """
        Defines the proxy host for HTTP traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "http".
        """
        self.__proxy = {
            **self.__proxy,
            "httpProxy": proxy,
        }
        return self

    def no_proxy(self, proxies: list):
        """
        Lists the address for which the proxy should be bypassed when the proxyType is "manual".

        proxies: A List containing any number of Strings.
        """
        self.__proxy = {
            **self.__proxy,
            "noProxy": proxies,
        }
        return self

    def ssl_proxy(self, proxy: str):
        """
        Defines the proxy host for encrypted TLS traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "https".
        """
        self.__proxy = {
            **self.__proxy,
            "sslProxy": proxy,
        }
        return self

    def socks_proxy(self, proxy: str):
        """
        Defines the proxy host for a SOCKS proxy when the proxyType is "manual".

        proxy: A host and optional port with an undefined scheme.
        """
        self.__proxy = {
            **self.__proxy,
            "socksProxy": proxy,
        }
        return self

    def socks_version(self, version: int):
        """
        Defines the SOCKS proxy version when the proxyType is "manual".

        version: Any integer between 0 and 255 inclusive.
        """
        self.__proxy = {
            **self.__proxy,
            "socksVersion": version,
        }
        return self

    def to_dict(self):
        return {"proxy": self.__proxy}


class TimeoutsBuilder:
    """
    Reference: https://www.w3.org/TR/webdriver/#dfn-session-script-timeout
    """

    def __init__(self) -> None:
        self.__timeouts = {}

    def implicit(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = math.ceil(timeout)
        self.__timeouts = {
            **self.__timeouts,
            "implicit": timeout,
        }
        return self

    def page_load(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = math.ceil(timeout)
        self.__timeouts = {
            **self.__timeouts,
            "pageLoad": timeout,
        }
        return self

    def script(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = math.ceil(timeout)
        self.__timeouts = {
            **self.__timeouts,
            "script": timeout,
        }
        return self

    def to_dict(self):
        return {"timeouts": self.__timeouts}


class Capabilities:
    """Reference: https://www.w3.org/TR/webdriver/#capabilities"""

    def __init__(self) -> None:
        self.desired_capabilities = {}
        # Used by subclasses
        self._driver_name = None

    def to_dict(self):
        raise NotImplementedError

    def browser_name(self, name: str):
        if not self._driver_name:
            self._driver_name = name
        self.desired_capabilities = {
            **self.desired_capabilities,
            "browserName": name,
        }
        return self

    def browser_version(self, version: str):
        self.desired_capabilities = {
            **self.desired_capabilities,
            "browserVersion": version,
        }
        return self

    def platform_name(self, name: str):
        """
        Identifies the operating system of the endpoint node.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "platformName": name,
        }
        return self

    def accept_insecure_certs(self, insecure: bool):
        """
        Indicates whether untrusted and self-signed TLS certificates are
        implicitly trusted on navigation for the duration of the session.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "acceptInsecureCerts": insecure,
        }
        return self

    def page_load_strategy(self, strategy: str):
        """
        strategy: normal, eager or none

        Reference: https://www.w3.org/TR/webdriver/#dfn-table-of-page-load-strategies
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "pageLoadStrategy": strategy,
        }
        return self

    def proxy(self, proxy_configuration: dict):
        """
        Defines the current session’s proxy configuration.
        Use the ProxyConfigurationBuilder class for simplicity.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            **proxy_configuration,
        }
        return self

    def set_window_rect(self, decison: bool):
        """
        Indicates whether the remote end supports all of the resizing and repositioning commands.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "setWindowRect": decison,
        }
        return self

    def timeouts(self, session_timeouts: dict):
        """
        Describes the timeouts imposed on certain session operations.
        Use the TimeoutsBuilder class for simplicity.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "timeouts": session_timeouts,
        }
        return self

    def strict_file_interactability(self, interactibility: bool):
        """
        Defines the current session’s strict file interactability.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "strictFileInteractability": interactibility,
        }
        return self

    def unhandled_prompt_behavior(self, behavior: str):
        """
        Describes the current session’s user prompt handler. Defaults to the 'dismiss and notify state'.

        behavior:
            "dismiss" All simple dialogs encountered should be dismissed.
            "accept" All simple dialogs encountered should be accepted.
            "dismiss and notify" All simple dialogs encountered should be dismissed, and an error returned that the dialog was handled.
            "accept and notify" All simple dialogs encountered should be accepted, and an error returned that the dialog was handled.
            "ignore" All simple dialogs encountered should be left to the user to handle.

        Reference: https://www.w3.org/TR/webdriver/#dfn-user-prompt-handler
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "unhandledPromptBehavior": behavior,
        }
        return self

    def user_agent(self, agent: str):
        """
        Identifies the default User-Agent value of the endpoint node.

        Reference: https://w3c.github.io/webdriver/#dfn-default-user-agent-value
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "userAgent": agent,
        }
        return self

    def headless(self):
        raise CapabilityNotSupported()

    def add_options(self, options: dict):
        """Add vendor options, for example
        {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}} or
        {"moz:experimental-webdriver": true}
        """
        self.desired_capabilities = {**self.desired_capabilities, **options}
        return self


class ChromeOptions:
    def __init__(self):
        """Builds the Chrome options

        Reference: https://developer.chrome.com/docs/chromedriver/capabilities#recognized_capabilities
        """
        self.options = {}

    def args(self, values: list):
        """
        List of command-line arguments to use when starting Chrome.
        Arguments with an associated value should be separated by
        a '=' sign (such as, ['start-maximized', 'user-data-dir=/tmp/temp_profile']).
        See a list of Chrome arguments.

        Reference: https://peter.sh/experiments/chromium-command-line-switches/
        """
        self.options = {**self.options, **{"args": values}}
        return self

    def binary(self, value: str):
        """
        Path to the Chrome executable to use.
        On macOS X, this should be the actual binary, not just the app, such as,
        /Applications/Google Chrome.app/Contents/MacOS/Google Chrome.
        """
        self.options = {**self.options, **{"binary": value}}
        return self

    def extensions(self, values: list[str]):
        """
        A list of Chrome extensions to install on startup. Each item in the list should be a base-64
        encoded packed Chrome extension (.crx)
        """
        self.options = {**self.options, **{"extensions": values}}
        return self

    def local_state(self, value: dict):
        """
        A dictionary with each entry consisting of the name of the preference and its value.
        These preferences are applied to the Local State file in the user data folder.
        """
        self.options = {**self.options, **{"localState": value}}
        return self

    def prefs(self, value: dict):
        """
            A dictionary with each entry consisting of the name of the preference and its value.
        These preferences are only applied to the user profile in use.
        See the 'Preferences' file in Chrome's user data directory for examples.
        """
        self.options = {**self.options, **{"prefs": value}}
        return self

    def detach(self, value: bool):
        self.options = {**self.options, **{"detach": value}}
        return self

    def debugger_address(self, value: str):
        self.options = {**self.options, **{"debuggerAddress": value}}
        return self

    def exclude_switches(self, values: list[str]):
        self.options = {**self.options, **{"excludeSwitches": values}}
        return self

    def minidump_path(self, value: str):
        self.options = {**self.options, **{"minidumpPath": value}}
        return self

    def mobile_emulation(self, value: dict):
        self.options = {**self.options, **{"mobileEmulation": value}}
        return self

    def perflogging_prefs(self, value: dict):
        self.options = {**self.options, **{"perfLoggingPrefs": value}}
        return self

    def windows_types(self, values: list[str]):
        self.options = {**self.options, **{"windowsTypes": values}}
        return self

    def to_dict(self):
        return {"goog:chromeOptions": self.options}


class ChromeCapabilities(Capabilities):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Returns the capabilities.
        """
        return {"desiredCapabilities": self.desired_capabilities}


class FirefoxCapabilities(Capabilities):
    def __init__(self):
        super().__init__()

    def always_match(self):
        self.options = {"alwaysMatch": self.to_dict()}
        return self

    def to_dict(self):
        """
        Returns the capabilities.
        """
        return {"capabilities": {"alwaysMatch": self.desired_capabilities}}


class FirefoxOptions(ChromeOptions):
    def __init__(self):
        super().__init__()

    def profile(self, value: str):
        self.options = {**self.options, **{"profile": value}}
        return self

    def log(self, value: dict):
        self.options = {**self.options, **{"log": value}}
        return self

    def env(self, value: dict):
        self.options = {**self.options, **{"env": value}}
        return self

    def level(self, value: str):
        self.options = {**self.options, **{"level": value}}
        return self


    def android_package(self, value: str):
        self.options = {**self.options, **{"androidPackage": value}}
        return self
    

    def android_activity(self, value: str):
        self.options = {**self.options, **{"androidActivity": value}}
        return self
    

    def android_device_serial(self, value: str):
        self.options = {**self.options, **{"androidDeviceSerial": value}}
        return self
    

    def android_intent_arguments(self, value: list[str]):
        self.options = {**self.options, **{"androidIntentArguments": value}}
        return self


    def to_dict(self):
        return {"moz:firefoxOptions": self.options}


class Server:
    """
    Starts and stops the local server. Cannot be used with remote servers

    Args:
        browser: if is `None`, then a simple `ChromeDriverManager` is used
        Reference: https://pypi.org/project/webdriver-manager/#use-with-chrome

        port: the port to start the local server
    """

    def __init__(self, browser: Union[DriverManager | None] = None, port=9999):
        self.__browser = browser
        self.__port = port
        self.__process = None
        self.__start()

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
                time.sleep(1)
                if i == (MAX_RETIES - 1):
                    self.__process.kill()
                    self.__process.wait()
                    raise Exception("Driver not started")

    def __start(self):
        driver_manager = self.__browser_factory()

        self.__process = subprocess.Popen(
            [driver_manager, f"--port={self.__port}"],
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
        )

        self.__wait_server()

    @property
    def url(self):
        """
        Returns the driver URL.
        """
        return f"http://localhost:{self.__port}"

    @property
    def process(self):
        return self.__process

    def dispose(self):
        """
        Dispose the driver process.
        """
        if self.__process:
            self.__process.kill()
            self.__process.wait()
            self.__process = None
