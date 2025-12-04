import pytest_asyncio
from pytest import fixture

from caqui import synchronous
from caqui.easy import AsyncPage
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"



@fixture(autouse=True, scope="session")
def setup_server():
    capabilities = (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .args(["headless"])
        .page_load_strategy("eager")
    )
    page = AsyncPage(SERVER_URL, capabilities, PAGE_URL)
    page.start()
    yield page
    page.dispose()




@pytest_asyncio.fixture
async def setup_functional_environment(setup_server: AsyncPage):
    await setup_server.get(PAGE_URL)
    yield setup_server
    try:
        await setup_server.alert.dismiss()
    except Exception:
        pass
    finally:
        setup_server.quit()


@pytest_asyncio.fixture
async def setup_environment(setup_server: AsyncPage):
    yield setup_server
    try:
        synchronous.dismiss_alert(setup_server.server_url, setup_server.session)
    except Exception:
        pass
    finally:
        setup_server.quit()
