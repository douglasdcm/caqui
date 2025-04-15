from caqui.by import By
from caqui import synchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.easy.capabilities import Capabilities, Browser, Server


@fixture
def __setup():
    server = Server()
    driver_url = server.url
    capabilities = (
        Capabilities()
        .browser_name(Browser.CHROME)
        .accept_insecure_certs(True)
        .additional_capability({"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}})
    ).to_dict()
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)
    server.dispose()


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
def test_locators(__setup, locator, value):
    assert synchronous.find_element(*__setup, locator, value) is not None
