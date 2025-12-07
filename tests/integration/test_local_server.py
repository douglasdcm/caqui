from pytest import fixture, mark

from caqui.easy.capabilities import (
    ChromeCapabilitiesBuilder,
    EdgeCapabilitiesBuilder,
    FirefoxCapabilitiesBuilder,
    OperaCapabilitiesBuilder,
)
from caqui.easy.drivers import AsyncDriver
from caqui.easy.server import LocalServer

PORT = 9998
SERVER_URL = f"http://localhost:{PORT}"


@fixture
async def setup_firefox():
    server = LocalServer()
    server.start_firefox()
    assert server.process is not None
    driver: AsyncDriver = await AsyncDriver(
        SERVER_URL, FirefoxCapabilitiesBuilder().args(["headless"]).level("info")
    ).get(SERVER_URL)
    yield driver
    await driver.quit()
    server.dispose()
    assert server.process is None


@fixture
async def setup_chrome():
    server = LocalServer()
    server.start_chrome()
    assert server.process is not None
    driver: AsyncDriver = await AsyncDriver(
        SERVER_URL, ChromeCapabilitiesBuilder().args(["headless"]).page_load_strategy("eager")
    ).get(SERVER_URL)
    yield driver
    await driver.quit()
    server.dispose()
    assert server.process is None


@fixture
async def setup_edge():
    server = LocalServer()
    server.start_edge()
    assert server.process is not None
    driver: AsyncDriver = await AsyncDriver(
        SERVER_URL, EdgeCapabilitiesBuilder().args(["headless"]).page_load_strategy("eager")
    ).get(SERVER_URL)
    yield driver
    await driver.quit()
    server.dispose()
    assert server.process is None


@fixture
async def setup_opera():
    server = LocalServer()
    server.start_opera()
    assert server.process is not None
    driver: AsyncDriver = await AsyncDriver(
        SERVER_URL, OperaCapabilitiesBuilder().args(["headless"]).page_load_strategy("eager")
    ).get(SERVER_URL)
    yield driver
    await driver.quit()
    server.dispose()
    assert server.process is None


def test_server_uses_firefox_webdriver_manager(setup_firefox):
    setup_firefox


def test_server_uses_chrome_webdriver_manager(setup_chrome):
    setup_chrome


# urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='msedgedriver.azureedge.net',
# port=443): Max retries exceeded with url: /LATEST_RELEASE_142_LINUX (Caused by
# NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7a6f35cf6630>:
# Failed to resolve 'msedgedriver.azureedge.net' ([Errno -2] Name or service not known)"))
# similar issue https://github.com/bonigarcia/webdrivermanager/issues/1513
@mark.skip(reason="Webdriver Manager issue")
def test_server_uses_edge_webdriver_manager(setup_edge):
    setup_edge


def test_server_uses_opera_webdriver_manager(setup_opera):
    setup_opera
