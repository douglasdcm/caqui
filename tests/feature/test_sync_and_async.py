from pytest import fixture, mark
from caqui import asynchronous, synchronous
from tests.constants import PAGE_URL


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "name": "webdriver",
            "browserName": "firefox",
            "marionette": True,
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


@mark.asyncio
async def test_set_timeouts(__setup):
    driver_url, session = __setup
    timeouts_1 = 5000  # milliseconds
    timeouts_2 = 3000  # milliseconds

    synchronous.set_timeouts(driver_url, session, timeouts_1)

    assert synchronous.get_timeouts(driver_url, session).get("implicit") == timeouts_1

    await asynchronous.set_timeouts(driver_url, session, timeouts_2)

    assert synchronous.get_timeouts(driver_url, session).get("implicit") == timeouts_2


@mark.asyncio
async def test_find_children_elements(__setup):
    driver_url, session = __setup
    expected = 5  # parent inclusive
    locator_type = "xpath"
    locator_value = "//div"

    parent_element = synchronous.find_element(
        driver_url, session, locator_type, '//div[@class="parent"]'
    )

    children_elements = synchronous.find_children_elements(
        driver_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) == expected

    children_elements = await asynchronous.find_children_elements(
        driver_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) == expected


@mark.asyncio
async def test_find_child_element(__setup):
    driver_url, session = __setup
    expected = "any4"
    locator_type = "xpath"
    locator_value = '//div[@class="child4"]'

    parent_element = synchronous.find_element(
        driver_url, session, locator_type, '//div[@class="parent"]'
    )

    child_element = synchronous.find_child_element(
        driver_url, session, parent_element, locator_type, locator_value
    )

    text = synchronous.get_text(driver_url, session, child_element)

    assert text == expected
    child_element = await asynchronous.find_child_element(
        driver_url, session, parent_element, locator_type, locator_value
    )
    text = synchronous.get_text(driver_url, session, child_element)
    assert text == expected


@mark.asyncio
async def test_get_page_source(__setup):
    driver_url, session = __setup
    expected = "Sample page"

    assert expected in synchronous.get_page_source(driver_url, session)
    assert expected in await asynchronous.get_page_source(driver_url, session)


@mark.asyncio
async def test_execute_script_asynchronous(__setup):
    driver_url, session = __setup
    script = "alert('any warn')"

    assert await asynchronous.execute_script(driver_url, session, script) == None


def test_execute_script_synchronous(__setup):
    driver_url, session = __setup
    script = "alert('any warn')"

    assert synchronous.execute_script(driver_url, session, script) == None


@mark.asyncio
async def test_get_alert_text(__setup):
    driver_url, session = __setup
    locator_type = "css selector"
    locator_value = "#alert-button"
    expected = "any warn"

    alert_button = synchronous.find_element(
        driver_url, session, locator_type, locator_value
    )
    synchronous.click(driver_url, session, alert_button)

    assert synchronous.get_alert_text(driver_url, session) == expected
    assert await asynchronous.get_alert_text(driver_url, session) == expected


@mark.asyncio
async def test_get_active_element(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, "any")

    assert synchronous.get_active_element(driver_url, session) == element
    assert await asynchronous.get_active_element(driver_url, session) == element


@mark.asyncio
async def test_clear_element(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"
    text = "any"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, text)
    assert synchronous.clear_element(driver_url, session, element) is True

    synchronous.send_keys(driver_url, session, element, text)
    assert await asynchronous.clear_element(driver_url, session, element) is True


@mark.asyncio
async def test_is_element_enabled(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.is_element_enabled(driver_url, session, element) is True
    assert await asynchronous.is_element_enabled(driver_url, session, element) is True


@mark.asyncio
async def test_get_css_value(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"
    property_name = "color"
    expected = "rgba(0, 0, 0, 1)"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert (
        synchronous.get_css_value(driver_url, session, element, property_name)
        == expected
    )
    assert (
        await asynchronous.get_css_value(driver_url, session, element, property_name)
        == expected
    )


@mark.asyncio
async def test_is_element_selected(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.is_element_selected(driver_url, session, element) is False
    assert await asynchronous.is_element_selected(driver_url, session, element) is False


@mark.asyncio
async def test_get_window_rectangle(__setup):
    driver_url, session = __setup
    expected = "height"

    assert expected in synchronous.get_window_rectangle(driver_url, session)
    rectangle = await asynchronous.get_window_rectangle(driver_url, session)
    assert expected in rectangle


@mark.asyncio
async def test_get_window_handles(__setup):
    driver_url, session = __setup

    assert isinstance(synchronous.get_window_handles(driver_url, session), list)
    handles = await asynchronous.get_window_handles(driver_url, session)
    assert isinstance(handles, list)


def test_close_window_sync(__setup):
    driver_url, session = __setup
    assert isinstance(synchronous.close_window(driver_url, session), list)


@mark.asyncio
async def test_close_window_async(__setup):
    driver_url, session = __setup

    response = await asynchronous.close_window(driver_url, session)
    assert isinstance(response, list)


@mark.asyncio
async def test_get_window(__setup):
    driver_url, session = __setup

    assert synchronous.get_window(driver_url, session) is not None
    assert await asynchronous.get_window(driver_url, session) is not None


@mark.asyncio
async def test_get_attribute(__setup):
    driver_url, session = __setup
    attribute = "href"
    element = synchronous.find_element(driver_url, session, "xpath", "//a[@id='a1']")

    assert (
        synchronous.get_attribute(driver_url, session, element, attribute)
        == "http://any1.com/"
    )
    assert (
        await asynchronous.get_attribute(driver_url, session, element, attribute)
        == "http://any1.com/"
    )


@mark.asyncio
async def test_get_cookies(__setup):
    driver_url, session = __setup

    assert isinstance(synchronous.get_cookies(driver_url, session), list)
    cookies = await asynchronous.get_cookies(driver_url, session)
    assert isinstance(cookies, list)


@mark.asyncio
async def test_go_back(__setup):
    driver_url, session = __setup

    assert synchronous.go_back(driver_url, session) is True
    assert await asynchronous.go_back(driver_url, session) is True


@mark.asyncio
async def test_get_url(__setup):
    driver_url, session = __setup
    expected = "playground.html"

    assert expected in synchronous.get_url(driver_url, session)
    assert expected in await asynchronous.get_url(driver_url, session)


@mark.asyncio
async def test_get_timeouts(__setup):
    driver_url, session = __setup
    expected = "implicit"

    assert expected in synchronous.get_timeouts(driver_url, session)
    assert expected in await asynchronous.get_timeouts(driver_url, session)


@mark.asyncio
async def test_get_status(__setup):
    driver_url, _ = __setup
    expected = "ready"
    assert expected in synchronous.get_status(driver_url).get("value")
    response = await asynchronous.get_status(driver_url)
    assert expected in response.get("value")


@mark.asyncio
async def test_get_title(__setup):
    driver_url, session = __setup
    expected = "Sample page"

    assert synchronous.get_title(driver_url, session) == expected
    assert await asynchronous.get_title(driver_url, session) == expected


@mark.asyncio
async def test_find_elements(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    elements = synchronous.find_elements(
        driver_url, session, locator_type, locator_value
    )
    async_elements = await asynchronous.find_elements(
        driver_url, session, locator_type, locator_value
    )

    assert len(elements) > 0
    assert len(async_elements) > 0


@mark.asyncio
async def test_find_element(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//input"

    assert (
        synchronous.find_element(driver_url, session, locator_type, locator_value)
        is not None
    )
    assert (
        await asynchronous.find_element(
            driver_url, session, locator_type, locator_value
        )
        is not None
    )


@mark.asyncio
async def test_get_property(__setup):
    driver_url, session = __setup
    text = "any_value"
    locator_type = "xpath"
    locator_value = "//input"
    property = "value"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, text)

    assert synchronous.get_property(driver_url, session, element, property) == text
    assert (
        await asynchronous.get_property(driver_url, session, element, property) == text
    )


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

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert (
        await asynchronous.send_keys(driver_url, session, element, text_async) is True
    )
    assert synchronous.send_keys(driver_url, session, element, text_sync) is True


@mark.asyncio
async def test_click(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.click(driver_url, session, element) is True
    assert synchronous.click(driver_url, session, element) is True
