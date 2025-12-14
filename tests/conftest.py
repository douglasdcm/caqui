import pytest_asyncio
from pytest import fixture

from caqui import asynchronous
from caqui.cdp.connection import CDPConnection
from caqui.easy.cdp.launcher import close_chrome, get_ws_url, launch_chrome
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from caqui.easy.cdp.drivers import AsyncDriver as AsyncDriverCDP
from caqui.easy.drivers import AsyncDriver
from caqui.easy.server import LocalServer
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


## CDP ##
@fixture(autouse=True, scope="session")
def launch_browser():
    launch_chrome()
    yield
    close_chrome()


@pytest_asyncio.fixture
async def setup_cdp_playground():
    # launch_chrome()
    async with CDPConnection(get_ws_url()) as conn:
        driver = AsyncDriverCDP(conn, PAGE_URL)
        await driver.get(PAGE_URL)
        await driver.set_window_size(1000, 1000)
        yield driver
        # await driver.close()
    # close_chrome()
