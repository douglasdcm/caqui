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

    def extensions(self, values: list):
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
        """If true, only quits if the session is quit or closed.
        If true and the session isn't quit."""
        self.options = {**self.options, **{"detach": value}}
        return self

    def debugger_address(self, value: str):
        """An address of a debugger server to connect to,
        in the form of <hostname/ip:port>, such as '127.0.0.1:38947'"""
        self.options = {**self.options, **{"debuggerAddress": value}}
        return self

    def exclude_switches(self, values: list):
        """List of command line switches to exclude that the Driver by default passes
        when starting Chrome."""
        self.options = {**self.options, **{"excludeSwitches": values}}
        return self

    def minidump_path(self, value: str):
        """Directory to store the driver minidumps."""
        self.options = {**self.options, **{"minidumpPath": value}}
        return self

    def mobile_emulation(self, value: dict):
        """A dictionary with either a value for "deviceName,"
        or values for "deviceMetrics", and "userAgent."
        """
        self.options = {**self.options, **{"mobileEmulation": value}}
        return self

    def perf_logging_prefs(self, value: dict):
        """The perfLoggingPrefs dictionary"""
        self.options = {**self.options, **{"perfLoggingPrefs": value}}
        return self

    def windows_types(self, values: list):
        """A list of window types that appear in the list of window handles."""
        self.options = {**self.options, **{"windowsTypes": values}}
        return self

    def to_dict(self):
        """Converts the options to a dict"""
        return {"goog:chromeOptions": self.options}


class ChromeOptionsBuilder(BaseOptions):
    pass


class EdgeOptionsBuilder(BaseOptions):
    def wdp_address(self, value: str):
        """An address of a Windows Device Portal server to connect to,
        in the form of hostname/ip:port, for example 127.0.0.1:50080"""
        self.options = {**self.options, **{"wdpAddress": value}}
        return self

    def wdp_password(self, value: str):
        """Optional password to use when connecting to a Windows Device Portal server.
        Required if the server has authentication enabled."""
        self.options = {**self.options, **{"wdpPassword": value}}
        return self

    def wdp_username(self, value: str):
        """Optional user name to use when connecting to a Windows Device Portal server.
        Required if the server has authentication enabled."""
        self.options = {**self.options, **{"wdpUsername": value}}
        return self

    def wdp_processId(self, value: str):
        """The required process ID to use if attaching to a running
        WebView2 UWP app, for example 36590."""
        self.options = {**self.options, **{"wdpProcessId": value}}
        return self

    def webview_options(self, value: str):
        """An optional dictionary that can be used to configure the WebView2
        environment when launching a WebView2 app."""
        self.options = {**self.options, **{"webviewOptions": value}}
        return self

    def windows_app(self, value: str):
        """Application user model ID of a Microsoft Edge app package to launch,
        for example `Microsoft.MicrosoftEdge.Stable_8wekyb3d8bbwe!MSEDGE.`"""
        self.options = {**self.options, **{"windowsApp": value}}
        return self

    def to_dict(self):
        """Converts the options to a dict"""
        return {"ms:edgeOptions": self.options}


class FirefoxOptions(BaseOptions):
    def __init__(self):
        super().__init__()

    def profile(self, value: str):
        """Base64-encoded ZIP of a profile directory to use for the Firefox instance."""
        self.options = {**self.options, **{"profile": value}}
        return self

    def log(self, value: dict):
        """To increase the logging verbosity of geckodriver and Firefox"""
        self.options = {**self.options, **{"log": value}}
        return self

    def env(self, value: dict):
        """Map of environment variable name to environment variable value"""
        self.options = {**self.options, **{"env": value}}
        return self

    def level(self, value: str):
        """Set the level of verbosity of geckodriver and Firefox.
        Available levels are `trace`, `debug`, `config`, `info`, `warn`, `error`, and `fatal`"""
        self.options = {**self.options, **{"level": value}}
        return self

    def android_package(self, value: str):
        """The package name of Firefox, e.g., `org.mozilla.firefox`, `org.mozilla.firefox_beta`,
        or `org.mozilla.fennec` depending on the release channel, or the package name of the
        application embedding GeckoView, e.g., `org.mozilla.geckoview_example`."""
        self.options = {**self.options, **{"androidPackage": value}}
        return self

    def android_activity(self, value: str):
        """The fully qualified class name of the activity to be launched"""
        self.options = {**self.options, **{"androidActivity": value}}
        return self

    def android_device_serial(self, value: str):
        """The serial number of the device on which to launch the application"""
        self.options = {**self.options, **{"androidDeviceSerial": value}}
        return self

    def android_intent_arguments(self, value: list):
        """Arguments to launch the intent with. Under the hood, geckodriver
        uses `Android am` to start the Android application under test."""
        self.options = {**self.options, **{"androidIntentArguments": value}}
        return self

    def to_dict(self):
        """Converts the options to a dict"""
        return {"moz:firefoxOptions": self.options}
