class BaseOptions:
    def __init__(self):
        """Builds the Chrome options

        Reference:
        https://developer.chrome.com/docs/chromedriver/capabilities#recognized_capabilities
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

    def perf_logging_prefs(self, value: dict):
        self.options = {**self.options, **{"perfLoggingPrefs": value}}
        return self

    def windows_types(self, values: list[str]):
        self.options = {**self.options, **{"windowsTypes": values}}
        return self

    def to_dict(self):
        return {"goog:chromeOptions": self.options}


class ChromeOptionsBuilder(BaseOptions):
    pass


class EdgeOptionsBuilder(BaseOptions):
    def wdp_address(self, value: str):
        self.options = {**self.options, **{"wdpAddress": value}}
        return self

    def wdp_password(self, value: str):
        self.options = {**self.options, **{"wdpPassword": value}}
        return self

    def wdp_username(self, value: str):
        self.options = {**self.options, **{"wdpUsername": value}}
        return self

    def wdp_processId(self, value: str):
        self.options = {**self.options, **{"wdpProcessId": value}}
        return self

    def webview_options(self, value: str):
        self.options = {**self.options, **{"webviewOptions": value}}
        return self

    def windows_app(self, value: str):
        self.options = {**self.options, **{"windowsApp": value}}
        return self


class FirefoxOptions(BaseOptions):
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
