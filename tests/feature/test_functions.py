from pytest import fixture, mark
from caqui import asynchronous, synchronous
from tests.constants import PAGE_URL


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
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


@mark.asyncio
async def test_get_property_value(__setup):
    driver_url, session = __setup
    text = "any_value"
    locator_type = "xpath"
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, text)

    assert synchronous.get_property_value(driver_url, session, element) == text
    assert await asynchronous.get_property_value(driver_url, session, element) == text


@mark.asyncio
async def test_get_text(__setup):
    driver_url, session = __setup
    expected = "end"
    locator_type = "xpath"
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.get_text(driver_url, session, element) == expected
    assert synchronous.get_text(driver_url, session, element) == expected


@mark.asyncio
async def test_send_keys(__setup):
    driver_url, session = __setup
    text_async = "any_async"
    text_sync = "any_sync"
    locator_type = "xpath"
    locator_value = "//input"
    expected = session

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert (
        await asynchronous.send_keys(driver_url, session, element, text_async)
        == expected
    )
    assert synchronous.send_keys(driver_url, session, element, text_sync) == expected


@mark.asyncio
async def test_click(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//button"
    expected = session

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.click(driver_url, session, element) == expected
    assert synchronous.click(driver_url, session, element) == expected
