# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from math import ceil
from typing import Union
from caqui.easy.options import BaseOptions


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
        self._proxy: dict = {}

    def proxy_type(self, proxy: str):
        """
        Indicates the type of proxy configuration.

        proxy: pac, direct, autodetect, system, or manual.

        Reference: https://www.w3.org/TR/webdriver/#dfn-proxy-configuration
        """
        self._proxy = {
            **self._proxy,
            "proxyType": proxy,
        }
        return self

    def proxy_autoconfig_url(self, url: str):
        """
        Defines the URL for a proxy auto-config file if proxyType is equal to "pac".
        """
        self._proxy = {
            **self._proxy,
            "proxyAutoconfigUrl": url,
        }
        return self

    def ftp_proxy(self, proxy: str):
        """
        Defines the proxy host for FTP traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "ftp".
        """
        self._proxy = {
            **self._proxy,
            "ftpProxy": proxy,
        }
        return self

    def http_proxy(self, proxy: str):
        """
        Defines the proxy host for HTTP traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "http".
        """
        self._proxy = {
            **self._proxy,
            "httpProxy": proxy,
        }
        return self

    def no_proxy(self, proxies: list):
        """
        Lists the address for which the proxy should be bypassed when the proxyType is "manual".

        proxies: A List containing any number of Strings.
        """
        self._proxy = {
            **self._proxy,
            "noProxy": proxies,
        }
        return self

    def ssl_proxy(self, proxy: str):
        """
        Defines the proxy host for encrypted TLS traffic when the proxyType is "manual".

        proxy: A host and optional port for scheme "https".
        """
        self._proxy = {
            **self._proxy,
            "sslProxy": proxy,
        }
        return self

    def socks_proxy(self, proxy: str):
        """
        Defines the proxy host for a SOCKS proxy when the proxyType is "manual".

        proxy: A host and optional port with an undefined scheme.
        """
        self._proxy = {
            **self._proxy,
            "socksProxy": proxy,
        }
        return self

    def socks_version(self, version: int):
        """
        Defines the SOCKS proxy version when the proxyType is "manual".

        version: Any integer between 0 and 255 inclusive.
        """
        self._proxy = {
            **self._proxy,
            "socksVersion": version,
        }
        return self

    def to_dict(self):
        return {"proxy": self._proxy}


class TimeoutsBuilder:
    """
    Reference: https://www.w3.org/TR/webdriver/#dfn-session-script-timeout
    """

    def __init__(self) -> None:
        self._timeouts: dict = {}

    def implicit(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = ceil(timeout)
        self._timeouts = {
            **self._timeouts,
            "implicit": timeout,
        }
        return self

    def page_load(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = ceil(timeout)
        self._timeouts = {
            **self._timeouts,
            "pageLoad": timeout,
        }
        return self

    def script(self, timeout: int):
        """Notice: if the number is a float, converts it to an integer"""
        timeout = ceil(timeout)
        self._timeouts = {
            **self._timeouts,
            "script": timeout,
        }
        return self

    def to_dict(self):
        return {"timeouts": self._timeouts}


class BaseCapabilities:
    """Reference: https://www.w3.org/TR/webdriver/#capabilities"""

    def __init__(self) -> None:
        self.desired_capabilities: dict = {}
        self.options: dict = {}

    def to_dict(self):
        raise NotImplementedError

    def browser_name(self, name: str):
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

    def proxy(self, proxy_configuration: Union[dict, ProxyConfigurationBuilder]):
        """
        Defines the current session’s proxy configuration.
        Use the ProxyConfigurationBuilder class for simplicity.
        """
        if isinstance(proxy_configuration, ProxyConfigurationBuilder):
            proxy_configuration = proxy_configuration.to_dict()
        self.desired_capabilities = {
            **self.desired_capabilities,
            **proxy_configuration,  # type: ignore
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

    def timeouts(self, session_timeouts: Union[dict, TimeoutsBuilder]):
        """
        Describes the timeouts imposed on certain session operations.
        Use the TimeoutsBuilder class for simplicity.
        """
        if isinstance(session_timeouts, TimeoutsBuilder):
            session_timeouts = session_timeouts.to_dict()
        self.desired_capabilities = {
            **self.desired_capabilities,
            **session_timeouts,  # type: ignore
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
        Describes the current session’s user prompt handler.
        Defaults to the 'dismiss and notify state'.

        behavior:
            "dismiss" All simple dialogs encountered should be dismissed.
            "accept" All simple dialogs encountered should be accepted.
            "dismiss and notify" All simple dialogs encountered should be dismissed,
              and an error returned that the dialog was handled.
            "accept and notify" All simple dialogs encountered should be accepted,
              and an error returned that the dialog was handled.
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

    def add_options(self, options: Union[dict, BaseOptions]):
        """Add vendor options, for example
        {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}} or
        {"moz:experimental-webdriver": true}
        """
        if isinstance(options, BaseOptions):
            options = options.to_dict()
        self.options = options
        return self


class ChromeCapabilitiesBuilder(BaseCapabilities):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Returns the capabilities.
        """
        self.desired_capabilities = {**self.desired_capabilities, **self.options}

        return {"desiredCapabilities": self.desired_capabilities}


class OperaCapabilitiesBuilder(ChromeCapabilitiesBuilder):
    pass


class FirefoxCapabilitiesBuilder(BaseCapabilities):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Returns the capabilities.
        """
        result = {"capabilities": self.desired_capabilities}
        if self.options:
            result["capabilities"] = {
                **result["capabilities"],
                **{"firstMatch": self.options},
            }
        return result
