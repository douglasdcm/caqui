import pytest_asyncio
from pytest import fixture

from caqui.cdp.asynchronous.connection import AsyncCDPConnection
from caqui.cdp.asynchronous.drivers import AsyncDriverCDP
from caqui.cdp.connection import SyncCDPConnection
from caqui.cdp.server import LocalServerCDP, get_ws_url
from caqui.cdp.synchronous.drivers import SyncDriverCDP
from caqui.webdriver.capabilities import ChromeCapabilitiesBuilder
from caqui.webdriver.drivers import AsyncDriver
from caqui.webdriver.server import LocalServer
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
TIMEOUTS = 2000


def _build_capabilities():
    # return OperaCapabilitiesBuilder().args(["headless"])
    # return FirefoxCapabilitiesBuilder().args(["headless"])
    # return EdgeCapabilitiesBuilder().args(["headless"])
    return (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .args(["headless"])
        .page_load_strategy("eager")
        .timeouts(TIMEOUTS, TIMEOUTS, TIMEOUTS)
    )


@fixture(autouse=True, scope="session")
def setup_server():
    server = LocalServer()
    # server.start()
    server.start_chrome()
    # server.start_firefox()
    # server.start_opera()
    # server.start_edge()
    # yield
    # server.dispose()


@pytest_asyncio.fixture
async def setup_playground():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    await async_driver.get(PAGE_URL)
    await async_driver.set_window_size(800, 600)
    yield async_driver
    # Necessary for some scenarios. For example, when the window of
    # Firefox is cloded, the session is closed to
    try:
        async_driver.quit()
    except Exception:
        pass


@fixture
def setup_functional_environment(setup_playground: AsyncDriver):
    server_url = setup_playground.server_url
    session = setup_playground.session
    yield server_url, session


@pytest_asyncio.fixture
async def setup_environment():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    yield async_driver
    try:
        async_driver.quit()
    except Exception:
        pass


# CDP
@fixture(autouse=True, scope="session")
def launch_browser():
    server = LocalServerCDP()
    server.start_chrome()
    yield server
    server.dispose()


@pytest_asyncio.fixture
async def setup_cdp_playground():
    async with AsyncCDPConnection(get_ws_url()) as conn:
        driver = AsyncDriverCDP(conn)
        await driver.get(PAGE_URL)
        await driver.set_window_size(1000, 1000)
        yield driver


@fixture
def setup_sync_cdp_playground():
    with SyncCDPConnection(get_ws_url()) as conn:
        driver = SyncDriverCDP(conn)
        driver.get(PAGE_URL)
        driver.set_window_size(1000, 1000)
        yield driver
