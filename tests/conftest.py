from time import sleep
from pytest import fixture
from tests.constants import PAGE_URL
from caqui.easy import AsyncPage
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from caqui.easy.options import ChromeOptionsBuilder
from caqui.easy.server import Server
from caqui import synchronous

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"


def __build_capabilities():
    options = ChromeOptionsBuilder().args(["headless"]).to_dict()
    capabilities = (
        ChromeCapabilitiesBuilder().accept_insecure_certs(True).add_options(options)
    ).to_dict()
    return capabilities


@fixture(autouse=True, scope="session")
def setup_server():
    server = Server.get_instance(port=SERVER_PORT)
    server.start()
    yield
    sleep(3)
    server.dispose()


@fixture
def setup_functional_environment():
    server_url = SERVER_URL
    capabilities = __build_capabilities()
    session = synchronous.get_session(server_url, capabilities)
    synchronous.go_to_page(
        server_url,
        session,
        PAGE_URL,
    )
    yield server_url, session
    try:
        synchronous.dismiss_alert(server_url, session)
    except Exception:
        pass
    try:
        synchronous.close_session(server_url, session)
    except Exception:
        pass


@fixture
def setup_environment():
    server_url = SERVER_URL
    capabilities = __build_capabilities()
    page = AsyncPage(server_url, capabilities, PAGE_URL)
    yield page
    try:
        synchronous.dismiss_alert(server_url, page.session)
    except Exception:
        pass
    page.quit()
