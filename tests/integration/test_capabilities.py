from pytest import mark
from caqui.by import By
from caqui.easy.capabilities import ChromeCapabilitiesBuilder, EdgeCapabilitiesBuilder, FirefoxCapabilitiesBuilder
from caqui.easy.drivers import AsyncDriver
from tests.constants import PAGE_URL

@mark.asyncio
async def test_capability_as_dictionary():
    SERVER_PORT = 9999
    SERVER_URL = f"http://localhost:{SERVER_PORT}"

    capabilities = {
        "capabilities": {
            "firstMatch": [
                {
                    "moz:firefoxOptions": {
                        "args": ["headless"],
                    }
                }
            ],
        }
    }
    driver = AsyncDriver(SERVER_URL, capabilities, specification="jsonwire")
    
    locator_type = By.XPATH
    locator_value = "//input"
    await driver.get(PAGE_URL)
    element = await driver.find_element(locator_type, locator_value)
    
    await element.click()
    assert await element.is_selected() is False


def test_firefox_capabilities_with_options():
    expected = {
        "capabilities": {
            "browserName": "any",
            "firstMatch": [
                {
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
                }
            ],
        }
    }
    capabilities = FirefoxCapabilitiesBuilder()
    (
        capabilities.browser_name("any")
        .binary("/usr/bin/firefox")
        .args(["headless", "profile"])
        .env({"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"})
        .log({"level": "trace"})
        .profile("any")
        .android_intent_arguments(["a", "b"])
        .android_activity("any")
        .android_device_serial("any")
        .android_package("any")
        .level("info")
    )
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
                "windowsTypes": ["any"],
                "perfLoggingPrefs": {
                    "enableNetwork": False,
                    "enablePage": False,
                    "traceCategories": "devtools.network",
                    "bufferUsageReportingInterval": 1000,
                },
            },
        }
    }
    capabilities = ChromeCapabilitiesBuilder()
    (
        capabilities.browser_name("any")
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
        .windows_types(["any"])
        .perf_logging_prefs(
            {
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
                "bufferUsageReportingInterval": 1000,
            }
        )
    )
    assert capabilities.to_dict() == expected



def test_edge_capabilities_with_options():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "ms:edgeOptions": {
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
                "windowsTypes": ["any"],
                "perfLoggingPrefs": {
                    "enableNetwork": False,
                    "enablePage": False,
                    "traceCategories": "devtools.network",
                    "bufferUsageReportingInterval": 1000,
                },
                "wdpAddress":"any",
                "wdpPassword":"any",
                "wdpUsername":"any",
                "wdpProcessId":"any",
                "webviewOptions":"any",
                "windowsApp":"any",
            },
        }
    }
    capabilities = EdgeCapabilitiesBuilder()
    (
        capabilities.browser_name("any")
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
        .windows_types(["any"])
        .perf_logging_prefs(
            {
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
                "bufferUsageReportingInterval": 1000,
            }
        )
        .wdp_address("any")
        .wdp_password("any")
        .wdp_username("any")
        .wdp_processId("any")
        .webview_options("any")
        .windows_app("any")
    )
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

    capabilities = (
        ChromeCapabilitiesBuilder()
        .browser_name("any")
        .accept_insecure_certs(True)
        .browser_version("any")
        .page_load_strategy("any")
        .platform_name("any")
        .timeouts(1,1,1)
        .set_window_rect(True)
        .strict_file_interactability(True)
        .timeouts(implicit=1, page_load=1, script=1)
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

    capabilities = (
        ChromeCapabilitiesBuilder()
        .browser_name("any")
        .accept_insecure_certs(True)
        .browser_version("any")
        .page_load_strategy("any")
        .platform_name("any")
        .proxy(
            ftp_proxy="any",
            http_proxy="str",
            no_proxy=["p1", "p2"],
            proxy_autoconfig_url="any",
            proxy_type="any",
            socks_proxy="any",
            socks_version=1,
            ssl_proxy="any",
        )
        .set_window_rect(True)
        .strict_file_interactability(True)
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
        .set_window_rect(True)
        .strict_file_interactability(True)
        .unhandled_prompt_behavior("any")
        .user_agent("any")
    )
    assert capabilities.to_dict() == expected
