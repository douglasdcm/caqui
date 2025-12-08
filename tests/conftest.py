import pytest_asyncio
from pytest import fixture

from caqui.easy.drivers import AsyncDriver
from caqui.easy.capabilities import ChromeCapabilitiesBuilder, FirefoxCapabilitiesBuilder
from caqui.easy.server import LocalServer
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
TIMEOUTS = 2000

def _build_capabilities():
    # return FirefoxCapabilitiesBuilder().args(["headless"])
    return (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .args(["headless", "verbose"])
        .page_load_strategy("eager")
        .timeouts(TIMEOUTS, TIMEOUTS, TIMEOUTS)
    )


@fixture(autouse=True, scope="session")
def setup_server():
    server = LocalServer()
    server.start_chrome()
    # server.start_firefox()
    # yield
    # server.dispose()


@pytest_asyncio.fixture
async def setup_playground():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    await async_driver.get(PAGE_URL)
    yield async_driver
    # Necessary for some scenarios. For example, when the window of
    # Firefox is cloded, the session is closed to
    try:
        async_driver.quit()
    except Exception:
        pass


@pytest_asyncio.fixture
async def setup_environment():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    yield async_driver
    try:
        async_driver.quit()
    except Exception:
        pass
