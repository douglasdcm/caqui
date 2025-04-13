from caqui.by import By
from caqui import synchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark
from caqui.easy.capabilities import CapabilitiesBuilder


@fixture
def __setup():
    capabilities = (
        CapabilitiesBuilder()
        .browser_name("chrome")
        .accept_insecure_certs(True)
        .additional_capability({"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}})
    ).build()
    driver_url = capabilities.driver_url
    session = synchronous.get_session(capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)
    capabilities.dispose()


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
