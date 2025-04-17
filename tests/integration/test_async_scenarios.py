from caqui import synchronous, asynchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.easy.capabilities import CapabilitiesBuilder, Browser
from caqui.easy.server import Server


@fixture
def __setup():
    server = Server()
    server_url = server.url
    capabilities = (
        CapabilitiesBuilder()
        .browser_name(Browser.CHROME)
        .accept_insecure_certs(True)
        .add_options({"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}})
    ).to_dict()
    session = synchronous.get_session(server_url, capabilities)
    synchronous.go_to_page(
        server_url,
        session,
        PAGE_URL,
    )
    yield server_url, session
    synchronous.close_session(server_url, session)
    server.dispose()


@mark.asyncio
async def test_get_all_links(__setup):
    server_url, session = __setup
    locator_type = "xpath"
    anchors = []

    for i in range(4):
        i += 1
        locator_value = f"//a[@id='a{i}']"
        anchor = synchronous.find_element(server_url, session, locator_type, locator_value)
        anchors.append(anchor)
        assert await asynchronous.get_text(server_url, session, anchors[i - 1]) == f"any{i}.com"
