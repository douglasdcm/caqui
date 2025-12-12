# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui


from typing import Dict, List


class BaseCapabilitiesBuilder:
    """Reference: https://www.w3.org/TR/webdriver/#capabilities"""
    def __init__(self) -> None:
        self.desired_capabilities: dict = {}
        self.options: dict = {}

    def browser_name(self, name: str):
        self.desired_capabilities = {
            **self.desired_capabilities,
            "browserName": name,
        }
        return self

    def browser_version(self, version: str):
        """
        Sets the desired browser version for the capabilities.

        Args:
            version (str): The version of the browser to be set.

        Returns:
            self: The instance of the class, allowing for method chaining.
        """
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
        Defines the current session’s page load strategy.
        strategy: normal, eager or none

        Reference: https://www.w3.org/TR/webdriver/#dfn-table-of-page-load-strategies
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "pageLoadStrategy": strategy,
        }
        return self

    def proxy(
        self,
        proxy_type: str,
        proxy_autoconfig_url: str,
        ftp_proxy: str,
        http_proxy: str,
        no_proxy: list,
        ssl_proxy: str,
        socks_proxy: str,
        socks_version: int,
    ):
        """
        This method sets up proxy settings for the WebDriver session according to the
        W3C WebDriver specification. It allows configuration of various proxy types
        and their respective settings.

        Args:
            proxy_type: The type of proxy to use (e.g., 'direct', 'manual',
            'pac', 'autodetect', 'system').
            proxy_autoconfig_url: URL of a proxy auto-config file to be used if proxyType is 'pac'.
            ftp_proxy: FTP proxy to be used for FTP traffic.
            http_proxy: HTTP proxy to be used for HTTP traffic.
            no_proxy: List of hostnames or IP addresses that should not be accessed through a proxy.
            ssl_proxy: HTTPS/SSL proxy to be used for secure traffic.
            socks_proxy: SOCKS proxy to be used for SOCKS traffic.
            socks_version: Version of SOCKS protocol to use (typically 4 or 5).

        Returns:
            The current BaseCapabilitiesBuilder instance to allow method chaining.

        Reference: https://www.w3.org/TR/webdriver/#dfn-proxy-configuration
        """
        proxy_configuration: dict = {
            "proxy": {
                "ftpProxy": ftp_proxy,
                "httpProxy": http_proxy,
                "noProxy": no_proxy,
                "proxyAutoconfigUrl": proxy_autoconfig_url,
                "proxyType": proxy_type,
                "socksProxy": socks_proxy,
                "socksVersion": socks_version,
                "sslProxy": ssl_proxy,
            },
        }
        self.desired_capabilities = {
            **self.desired_capabilities,
            **proxy_configuration,
        }
        return self

    def set_window_rect(self, decison: bool):
        """
        Set the window rect capability for the remote end.

        Indicates whether the remote end supports all of the resizing and repositioning
        commands, including maximizing, minimizing, fullscreen, and moving the window.

        Args:
            decison: A boolean flag indicating whether window rect capability is supported.

        Returns:
            The current instance for method chaining.
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "setWindowRect": decison,
        }
        return self

    def timeouts(self, implicit: int, page_load: int, script: int):
        """
        Describes the timeouts imposed on certain session operations.

        Args:
            implicit: The number of milliseconds to wait when attempting to find an element.
            page_load: The number of milliseconds to wait for a page load to complete before
            returning an error.
            script: The number of milliseconds to wait for an asynchronous script to finish
            execution before returning an error.
        Returns:
            Self instance for method chaining.

        Reference: https://www.w3.org/TR/webdriver/#dfn-session-script-timeout
        """
        self.desired_capabilities = {
            **self.desired_capabilities,
            "timeouts": {
                "implicit": implicit,
                "pageLoad": page_load,
                "script": script,
            },
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

    def to_dict(self) -> dict:
        raise NotImplementedError("Need to be implemented in subclasses")


class ChromeCapabilitiesBuilder(BaseCapabilitiesBuilder):
    OPTIONS = "goog:chromeOptions"

    def __init__(self):
        super().__init__()
        self.options = {ChromeCapabilitiesBuilder.OPTIONS: {}}

    def detach(self, value: bool) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["detach"] = value
        return self

    def binary(self, value: str) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["binary"] = value
        return self

    def extensions(self, value: List[str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["extensions"] = value
        return self

    def debugger_address(self, value: str) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["debuggerAddress"] = value
        return self

    def exclude_switches(self, value: List[str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["excludeSwitches"] = value
        return self

    def minidump_path(self, value: str) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["minidumpPath"] = value
        return self

    def windows_types(self, value: List[str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["windowsTypes"] = value
        return self

    def mobile_emulation(self, value: Dict[str, str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["mobileEmulation"] = value
        return self

    def local_state(self, value: Dict[str, str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["localState"] = value
        return self

    def args(self, value: List[str]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["args"] = value
        return self

    def prefs(self, value: Dict[str, bool]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["prefs"] = value
        return self

    def perf_logging_prefs(self, value: Dict[str, object]) -> "ChromeCapabilitiesBuilder":
        self.options[ChromeCapabilitiesBuilder.OPTIONS]["perfLoggingPrefs"] = value
        return self

    def to_dict(self) -> dict:
        """
        Returns the capabilities.
        """
        if self.options[ChromeCapabilitiesBuilder.OPTIONS]:
            return {"desiredCapabilities": {**self.desired_capabilities, **self.options}}
        return {
            "desiredCapabilities": {
                **self.desired_capabilities,
            }
        }


class EdgeCapabilitiesBuilder(BaseCapabilitiesBuilder):
    OPTIONS = "ms:edgeOptions"

    def __init__(self):
        super().__init__()
        self.options = {EdgeCapabilitiesBuilder.OPTIONS: {}}

    def perf_logging_prefs(self, value: Dict[str, object]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["perfLoggingPrefs"] = value
        return self

    def detach(self, value: str) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["detach"] = value
        return self

    def binary(self, value: bool) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["binary"] = value
        return self

    def extensions(self, value: List[str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["extensions"] = value
        return self

    def debugger_address(self, value: str) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["debuggerAddress"] = value
        return self

    def exclude_switches(self, value: List[str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["excludeSwitches"] = value
        return self

    def minidump_path(self, value: str) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["minidumpPath"] = value
        return self

    def windows_types(self, value: List[str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["windowsTypes"] = value
        return self

    def mobile_emulation(self, value: Dict[str, str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["mobileEmulation"] = value
        return self

    def local_state(self, value: Dict[str, str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["localState"] = value
        return self

    def args(self, value: List[str]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["args"] = value
        return self

    def prefs(self, value: Dict[str, bool]) -> "EdgeCapabilitiesBuilder":
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["prefs"] = value
        return self

    # More options
    def wdp_address(self, value: str) -> "EdgeCapabilitiesBuilder":
        """An address of a Windows Device Portal server to connect to,
        in the form of hostname/ip:port, for example 127.0.0.1:50080"""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["wdpAddress"] = value
        return self

    def wdp_password(self, value: str) -> "EdgeCapabilitiesBuilder":
        """Optional password to use when connecting to a Windows Device Portal server.
        Required if the server has authentication enabled."""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["wdpPassword"] = value
        return self

    def wdp_username(self, value: str) -> "EdgeCapabilitiesBuilder":
        """Optional user name to use when connecting to a Windows Device Portal server.
        Required if the server has authentication enabled."""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["wdpUsername"] = value
        return self

    def wdp_processId(self, value: str) -> "EdgeCapabilitiesBuilder":
        """The required process ID to use if attaching to a running
        WebView2 UWP app, for example 36590."""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["wdpProcessId"] = value
        return self

    def webview_options(self, value: str) -> "EdgeCapabilitiesBuilder":
        """An optional dictionary that can be used to configure the WebView2
        environment when launching a WebView2 app."""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["webviewOptions"] = value
        return self

    def windows_app(self, value: str) -> "EdgeCapabilitiesBuilder":
        """Application user model ID of a Microsoft Edge app package to launch,
        for example `Microsoft.MicrosoftEdge.Stable_8wekyb3d8bbwe!MSEDGE.`"""
        self.options[EdgeCapabilitiesBuilder.OPTIONS]["windowsApp"] = value
        return self

    def to_dict(self) -> dict:
        """Converts the options to a dict"""
        if self.options[EdgeCapabilitiesBuilder.OPTIONS]:
            return {"desiredCapabilities": {**self.desired_capabilities, **self.options}}
        return {
            "desiredCapabilities": {
                **self.desired_capabilities,
            }
        }


class OperaCapabilitiesBuilder(ChromeCapabilitiesBuilder):
    pass


class FirefoxCapabilitiesBuilder(BaseCapabilitiesBuilder):
    OPTIONS = "moz:firefoxOptions"

    def __init__(self):
        super().__init__()
        self.options = {"moz:firefoxOptions": {}}

    def detach(self, value: bool) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["detach"] = value
        return self

    def binary(self, value: str) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["binary"] = value
        return self

    def extensions(self, value: List[str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["extensions"] = value
        return self

    def debugger_address(self, value: str) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["debuggerAddress"] = value
        return self

    def exclude_switches(self, value: List[str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["excludeSwitches"] = value
        return self

    def minidump_path(self, value: str) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["minidumpPath"] = value
        return self

    def windows_types(self, value: List[str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["windowsTypes"] = value
        return self

    def mobile_emulation(self, value: Dict[str, str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["mobileEmulation"] = value
        return self

    def local_state(self, value: Dict[str, str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["localState"] = value
        return self

    def args(self, value: List[str]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["args"] = [f"-{arg}" for arg in value]
        return self

    def prefs(self, value: Dict[str, bool]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["prefs"] = value
        return self

    def perf_logging_prefs(self, value: Dict[str, object]) -> "FirefoxCapabilitiesBuilder":
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["perfLoggingPrefs"] = value
        return self

    def profile(self, value: str) -> "FirefoxCapabilitiesBuilder":
        """Base64-encoded ZIP of a profile directory to use for the Firefox instance."""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["profile"] = value
        return self

    def log(self, value: dict) -> "FirefoxCapabilitiesBuilder":
        """To increase the logging verbosity of geckodriver and Firefox"""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["log"] = value
        return self

    def env(self, value: dict) -> "FirefoxCapabilitiesBuilder":
        """Map of environment variable name to environment variable value"""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["env"] = value
        return self

    def level(self, value: str) -> "FirefoxCapabilitiesBuilder":
        """Set the level of verbosity of geckodriver and Firefox.
        Available levels are `trace`, `debug`, `config`, `info`, `warn`, `error`, and `fatal`"""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["level"] = value
        return self

    def android_package(self, value: str) -> "FirefoxCapabilitiesBuilder":
        """The package name of Firefox, e.g., `org.mozilla.firefox`, `org.mozilla.firefox_beta`,
        or `org.mozilla.fennec` depending on the release channel, or the package name of the
        application embedding GeckoView, e.g., `org.mozilla.geckoview_example`."""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["androidPackage"] = value
        return self

    def android_activity(self, value: str) -> "FirefoxCapabilitiesBuilder":
        """The fully qualified class name of the activity to be launched"""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["androidActivity"] = value
        return self

    def android_device_serial(self, value: str) -> "FirefoxCapabilitiesBuilder":
        """The serial number of the device on which to launch the application"""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["androidDeviceSerial"] = value
        return self

    def android_intent_arguments(self, value: list) -> "FirefoxCapabilitiesBuilder":
        """Arguments to launch the intent with. Under the hood, geckodriver
        uses `Android am` to start the Android application under test."""
        self.options[FirefoxCapabilitiesBuilder.OPTIONS]["androidIntentArguments"] = value
        return self

    def to_dict(self) -> dict:
        """
        Returns the capabilities.
        """
        result = {"capabilities": self.desired_capabilities}
        if self.options[FirefoxCapabilitiesBuilder.OPTIONS]:
            result["capabilities"] = {
                **result["capabilities"],
                "firstMatch": [self.options],
            }
        return result
