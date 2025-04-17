from caqui.by import By
from caqui import synchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.easy.capabilities import Browser, ChromeCapabilitiesBuilder
from caqui.easy.server import Server


# @fixture
# def setup_functional_environment():
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


@mark.parametrize(
    "locator, value",
    [
        (By.CLASS_NAME, "my-class"),
        (By.CSS_SELECTOR, ".my-class"),
        (By.ID, "button"),
        (By.LINK_TEXT, "any2.com"),
        (By.NAME, "fname"),
        (By.PARTIAL_LINK_TEXT, "any3"),
        (By.TAG_NAME, "input"),
        (By.XPATH, "//button"),
    ],
)
def test_locators(setup_functional_environment, locator, value):
    assert synchronous.find_element(*setup_functional_environment, locator, value) is not None
