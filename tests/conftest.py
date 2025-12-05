import pytest_asyncio
from pytest import fixture
from caqui.easy import AsyncDriver
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from caqui.easy.server import LocalServer
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def _build_capabilities():
    return (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .args(["headless", "verbose"])
        .page_load_strategy("eager")
    )

@fixture(autouse=True, scope="session")
def setup_server():
    server = LocalServer()
    server.start_chrome()
    # yield
    # server.dispose()


@pytest_asyncio.fixture
async def setup_playground():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    await async_driver.get(PAGE_URL)
    yield async_driver
    async_driver.quit()



@pytest_asyncio.fixture
async def setup_environment():
    async_driver = AsyncDriver(SERVER_URL, _build_capabilities())
    yield async_driver
    async_driver.quit()
