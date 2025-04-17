from caqui import synchronous, asynchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.easy.capabilities import BaseCapabilities, Browser, ChromeCapabilitiesBuilder
from caqui.easy.server import Server


# @fixture
# def setup_environment():
#     server = Server()
#     server.start()
#     server_url = server.url
#     capabilities = (
#         ChromeCapabilitiesBuilder()
#         .browser_name(Browser.CHROME)
#         .accept_insecure_certs(True)
#         .add_options({"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}})
#     ).to_dict()
#     session = synchronous.get_session(server_url, capabilities)
#     synchronous.go_to_page(
#         server_url,
#         session,
#         PAGE_URL,
#     )
#     yield server_url, session
#     synchronous.close_session(server_url, session)
#     server.dispose()


@mark.asyncio
async def test_get_all_links(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "xpath"
    anchors = []

    for i in range(4):
        i += 1
        locator_value = f"//a[@id='a{i}']"
        anchor = synchronous.find_element(server_url, session, locator_type, locator_value)
        anchors.append(anchor)
        assert await asynchronous.get_text(server_url, session, anchors[i - 1]) == f"any{i}.com"
