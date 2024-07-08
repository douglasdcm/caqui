import math


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

    def build(self):
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

    def build(self):
        return {"timeouts": self.__timeouts}


class CapabilitiesBuilder:
    """Reference: https://www.w3.org/TR/webdriver/#capabilities"""

    def __init__(self) -> None:
        self.__desired_capabilities = {}

    def browser_name(self, name: str):
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "browserName": name,
        }
        return self

    def browser_version(self, version: str):
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "browserVersion": version,
        }
        return self

    def platform_name(self, name: str):
        """
        Identifies the operating system of the endpoint node.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "platformName": name,
        }
        return self

    def accept_insecure_certs(self, insecure: bool):
        """
        Indicates whether untrusted and self-signed TLS certificates are
        implicitly trusted on navigation for the duration of the session.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "acceptInsecureCerts": insecure,
        }
        return self

    def page_load_strategy(self, strategy: str):
        """
        strategy: normal, eager or none

        Reference: https://www.w3.org/TR/webdriver/#dfn-table-of-page-load-strategies
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "pageLoadStrategy": strategy,
        }
        return self

    def proxy(self, proxy_configuration: dict):
        ProxyConfigurationBuilder
        """
        Defines the current session’s proxy configuration.
        Use the ProxyConfigurationBuilder class for simplicity.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            **proxy_configuration,
        }
        return self

    def set_window_rect(self, decison: bool):
        """
        Indicates whether the remote end supports all of the resizing and repositioning commands.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "setWindowRect": decison,
        }
        return self

    def timeouts(self, session_timeouts: dict):
        """
        Describes the timeouts imposed on certain session operations.
        Use the TimeoutsBuilder class for simplicity.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "timeouts": session_timeouts,
        }
        return self

    def strict_file_interactability(self, interactibility: bool):
        """
        Defines the current session’s strict file interactability.
        """
        self.__desired_capabilities = {
            **self.__desired_capabilities,
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
        self.__desired_capabilities = {
            **self.__desired_capabilities,
            "unhandledPromptBehavior": behavior,
        }
        return self

    def additional_capability(self, capabilitiy: dict):
        """Add any capability, for example
        {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}} or
        {"moz:experimental-webdriver": true}
        """
        self.__desired_capabilities = {**self.__desired_capabilities, **capabilitiy}
        return self

    def build(self):
        return {"desiredCapabilities": self.__desired_capabilities}
