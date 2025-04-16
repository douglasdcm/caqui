from pytest import mark, fixture
from caqui.easy.capabilities import (
    Capabilities, FirefoxOptions, Server, ChromeOptions, FirefoxCapabilities, ChromeCapabilities)
from caqui.easy.page import AsyncPage
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def __setup_environment(options):
    if isinstance(options, ChromeOptions):
        server = Server()
        capabilities = ChromeCapabilities()
    if isinstance(options, FirefoxOptions):
        server = Server(GeckoDriverManager(), port=9998)
        capabilities = FirefoxCapabilities()
    capabilities = (capabilities.add_options(options.to_dict())).to_dict()
    driver = AsyncPage(server.url, capabilities)
    return server, driver

@fixture
def setup_firefox_options():
    options = (
        FirefoxOptions()
        # .args(["-headless", "-profile"])
        # .env({"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"})
        # .log({"level": "trace"})
        # .profile("any")
        # .android_intent_arguments(["a", "b"])
        # .android_activity("any")
        # .android_device_serial("any")
        # .android_package("any")
        # .level("info")
    )

    server, driver = __setup_environment(options)
    yield options, driver
    driver.quit()
    server.dispose()


@fixture
def setup_chrome_options():
    options = (
        ChromeOptions()
        .args(["headless"])
        .prefs({"javascript.options.showInConsole": False})
        .detach(True)
        ## Other examples
        # .binary("/path/to/chrome/executable")
        # .extensions(["ext1", "ext2"])
        # .local_state({"any": "any"})
        # .debugger_address("127.0.0.1:9999")
        # .exclude_switches(["sw1", "sw2"])
        # .minidump_path("any")
        # .mobile_emulation({"any": "any"})
        # .windows_types("any")
        # .perflogging_prefs({
        #     "enableNetwork": False,
        #     "enablePage": False,
        #     "traceCategories": "devtools.network",
        #     "bufferUsageReportingInterval": 1000
        #     })
    )

    server, driver = __setup_environment(options)
    yield options, driver
    driver.quit()
    server.dispose()

@mark.asyncio
async def test_firefox_options():
    expected_options = {
        "moz:firefoxOptions": {
            "args": ["-headless", "-profile"],
            "prefs": {"dom.ipc.processCount": 8, "javascript.options.showInConsole": False},
            "log": {"level": "trace"},
            "env": {"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"},
        }
    }
    expected = {"capabilities": {"alwaysMatch": {**expected_options}}}
    Server(GeckoDriverManager(), port=9998)
    options = (
        FirefoxOptions()
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

    f = FirefoxCapabilities()
    f.add_options(options.to_dict())

    assert f.to_dict() == 42

    assert options.to_dict() == expected_options
    # options, driver = setup_firefox_options
    # assert options.to_dict() == expected
    # await driver.get("https://example.com")

@mark.asyncio
async def test_chrome_options(setup_chrome_options):
    expected = {
        "goog:chromeOptions": {
            "args": [
                "headless",
            ],
            "detach": True,
            "prefs": {"javascript.options.showInConsole": False},
        }
    }
    options, driver = setup_chrome_options
    assert options.to_dict() == expected
    await driver.get("https://example.com")
