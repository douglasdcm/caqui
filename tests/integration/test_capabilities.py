from caqui.easy.capabilities import (
    FirefoxCapabilitiesBuilder,
    ChromeCapabilitiesBuilder,
    ProxyConfigurationBuilder,
    TimeoutsBuilder,
)
from caqui.easy.options import ChromeOptionsBuilder, FirefoxOptions


def test_firefox_capabilities_with_options():
    expected = {
        "capabilities": {
            "browserName": "any",
            "firstMatch": {
                "moz:firefoxOptions": {
                    "binary": "/usr/bin/firefox",
                    "args": ["-headless", "-profile"],
                    "env": {"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"},
                    "log": {"level": "trace"},
                    "profile": "any",
                    "androidIntentArguments": ["a", "b"],
                    "androidActivity": "any",
                    "androidDeviceSerial": "any",
                    "androidPackage": "any",
                    "level": "info",
                }
            },
        }
    }
    options = (
        FirefoxOptions()
        .binary("/usr/bin/firefox")
        .args(["-headless", "-profile"])
        .env({"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"})
        .log({"level": "trace"})
        .profile("any")
        .android_intent_arguments(["a", "b"])
        .android_activity("any")
        .android_device_serial("any")
        .android_package("any")
        .level("info")
    )
    capabilities = FirefoxCapabilitiesBuilder()
    capabilities.browser_name("any")
    capabilities.add_options(options.to_dict())
    assert capabilities.to_dict() == expected


def test_chrome_capabilities_with_options():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "goog:chromeOptions": {
                "args": ["headless"],
                "prefs": {"javascript.options.showInConsole": False},
                "detach": True,
                "binary": "/path/to/chrome/executable",
                "extensions": ["ext1", "ext2"],
                "localState": {"any": "any"},
                "debuggerAddress": "127.0.0.1:9999",
                "excludeSwitches": ["sw1", "sw2"],
                "minidumpPath": "any",
                "mobileEmulation": {"any": "any"},
                "windowsTypes": "any",
                "perfLoggingPrefs": {
                    "enableNetwork": False,
                    "enablePage": False,
                    "traceCategories": "devtools.network",
                    "bufferUsageReportingInterval": 1000,
                },
            },
        }
    }
    options = (
        ChromeOptionsBuilder()
        .args(["headless"])
        .prefs({"javascript.options.showInConsole": False})
        .detach(True)
        # Other examples
        .binary("/path/to/chrome/executable")
        .extensions(["ext1", "ext2"])
        .local_state({"any": "any"})
        .debugger_address("127.0.0.1:9999")
        .exclude_switches(["sw1", "sw2"])
        .minidump_path("any")
        .mobile_emulation({"any": "any"})
        .windows_types("any")
        .perf_logging_prefs(
            {
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
                "bufferUsageReportingInterval": 1000,
            }
        )
    )
    capabilities = ChromeCapabilitiesBuilder()
    capabilities.browser_name("any")
    capabilities.add_options(options.to_dict())
    assert capabilities.to_dict() == expected


def test_standard_capabilities_with_timeout():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "acceptInsecureCerts": True,
            "browserVersion": "any",
            "pageLoadStrategy": "any",
            "platformName": "any",
            "setWindowRect": True,
            "strictFileInteractability": True,
            "timeouts": {"implicit": 1, "pageLoad": 1, "script": 1},
            "unhandledPromptBehavior": "any",
            "userAgent": "any",
        }
    }

    timeout = TimeoutsBuilder().implicit(1).page_load(1).script(1)

    capabilities = (
        ChromeCapabilitiesBuilder()
        .browser_name("any")
        .accept_insecure_certs(True)
        .browser_version("any")
        .page_load_strategy("any")
        .platform_name("any")
        .proxy({})
        .set_window_rect(True)
        .strict_file_interactability(True)
        .timeouts(timeout.to_dict())
        .unhandled_prompt_behavior("any")
        .user_agent("any")
    )
    assert capabilities.to_dict() == expected


def test_standard_capabilities_with_proxy():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "acceptInsecureCerts": True,
            "browserVersion": "any",
            "pageLoadStrategy": "any",
            "platformName": "any",
            "proxy": {
                "ftpProxy": "any",
                "httpProxy": "str",
                "noProxy": ["p1", "p2"],
                "proxyAutoconfigUrl": "any",
                "proxyType": "any",
                "socksProxy": "any",
                "socksVersion": 1,
                "sslProxy": "any",
            },
            "setWindowRect": True,
            "strictFileInteractability": True,
            "unhandledPromptBehavior": "any",
            "userAgent": "any",
        }
    }

    proxy = (
        ProxyConfigurationBuilder()
        .ftp_proxy("any")
        .http_proxy("str")
        .no_proxy(["p1", "p2"])
        .proxy_autoconfig_url("any")
        .proxy_type("any")
        .socks_proxy("any")
        .socks_version(1)
        .ssl_proxy("any")
    )

    capabilities = (
        ChromeCapabilitiesBuilder()
        .browser_name("any")
        .accept_insecure_certs(True)
        .browser_version("any")
        .page_load_strategy("any")
        .platform_name("any")
        .proxy(proxy.to_dict())
        .set_window_rect(True)
        .strict_file_interactability(True)
        .timeouts({})
        .unhandled_prompt_behavior("any")
        .user_agent("any")
    )
    assert capabilities.to_dict() == expected


def test_standard_capabilities():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "acceptInsecureCerts": True,
            "browserVersion": "any",
            "pageLoadStrategy": "any",
            "platformName": "any",
            "setWindowRect": True,
            "strictFileInteractability": True,
            "unhandledPromptBehavior": "any",
            "userAgent": "any",
        }
    }

    capabilities = (
        ChromeCapabilitiesBuilder()
        .browser_name("any")
        .accept_insecure_certs(True)
        .browser_version("any")
        .page_load_strategy("any")
        .platform_name("any")
        .proxy({})
        .set_window_rect(True)
        .strict_file_interactability(True)
        .timeouts({})
        .unhandled_prompt_behavior("any")
        .user_agent("any")
    )
    assert capabilities.to_dict() == expected
