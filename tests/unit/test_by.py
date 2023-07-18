from caqui import by
from pytest import fixture, mark, raises
from caqui import asynchronous, synchronous
from tests.constants import PAGE_URL
from caqui.exceptions import WebDriverError


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "name": "webdriver",
            "browserName": "chrome",
            "marionette": False,
            "acceptInsecureCerts": True,
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)


@mark.parametrize(
    "locator, value",
    [
        (by.CLASS_NAME, "my-class"),
        (by.CSS_SELECTOR, ".my-class"),
        (by.ID, "button"),
        (by.LINK_TEXT, "any2.com"),
        (by.NAME, "fname"),
        (by.PARTIAL_LINK_TEXT, "any3"),
        (by.TAG_NAME, "input"),
        (by.XPATH, "//button"),
    ],
)
def test_locators(__setup, locator, value):
    assert synchronous.find_element(*__setup, locator, value) is not None
