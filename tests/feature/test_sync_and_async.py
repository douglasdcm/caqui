from pytest import fixture, mark, raises
from caqui import asynchronous, synchronous
from tests.constants import PAGE_URL
from caqui.exceptions import WebDriverError
from caqui.by import By
from caqui.easy.capabilities import CapabilitiesBuilder


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = (
        CapabilitiesBuilder()
        .browser_name("chrome")
        .accept_insecure_certs(True)
        .additional_capability(
            {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
        )
    ).build()
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)


@mark.asyncio
async def test_add_cookie(__setup):
    driver_url, session = __setup
    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    synchronous.go_to_page(
        driver_url,
        session,
        "http://www.google.com",
    )
    cookies_before = synchronous.get_cookies(driver_url, session)

    cookie = cookies_before[0]
    cookie["name"] = "other"

    assert synchronous.add_cookie(driver_url, session, cookie) is True
    cookies_after = synchronous.get_cookies(driver_url, session)
    assert len(cookies_after) > len(cookies_before)

    cookies_before = cookies_after
    cookie = cookies_before[0]
    cookie[By.NAME] = "another"

    assert await asynchronous.add_cookie(driver_url, session, cookie) is True
    cookies_after = synchronous.get_cookies(driver_url, session)
    assert len(cookies_after) > len(cookies_before)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookie_asynchronous(__setup):
    driver_url, session = __setup
    cookies = synchronous.get_cookies(driver_url, session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert await asynchronous.delete_cookie(driver_url, session, name) is True
    cookies = synchronous.get_cookies(driver_url, session)
    assert len(cookies) == zero


@mark.skip(reason="works just in firefox")
@mark.asyncio
def test_delete_cookie_synchronous(__setup):
    driver_url, session = __setup
    cookies = synchronous.get_cookies(driver_url, session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert synchronous.delete_cookie(driver_url, session, name) is True
    cookies = synchronous.get_cookies(driver_url, session)
    assert len(cookies) == zero


@mark.asyncio
async def test_refresh_page(__setup):
    driver_url, session = __setup

    element_before = synchronous.find_element(driver_url, session, By.XPATH, "//input")
    assert (
        synchronous.refresh_page(
            driver_url,
            session,
        )
        is True
    )

    element_after = synchronous.find_element(driver_url, session, By.XPATH, "//input")
    assert element_before != element_after

    element_before = element_after
    assert await asynchronous.refresh_page(driver_url, session) is True

    element_after = synchronous.find_element(driver_url, session, By.XPATH, "//input")
    assert element_before != element_after


@mark.asyncio
async def test_go_forward(__setup):
    driver_url, session = __setup
    title = "Sample page"

    synchronous.go_back(driver_url, session)
    assert (
        synchronous.go_forward(
            driver_url,
            session,
        )
        is True
    )
    assert synchronous.get_title(driver_url, session) == title

    synchronous.go_back(driver_url, session)
    assert await asynchronous.go_forward(driver_url, session) is True
    assert synchronous.get_title(driver_url, session) == title


@mark.asyncio
async def test_set_window_rectangle(__setup):
    driver_url, session = __setup
    width = 500
    height = 300
    x = 10
    y = 20
    window_rectangle_before = synchronous.get_window_rectangle(driver_url, session)

    assert (
        synchronous.set_window_rectangle(driver_url, session, width, height, x, y)
        is True
    )

    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")

    synchronous.maximize_window(driver_url, session)

    assert (
        await asynchronous.set_window_rectangle(
            driver_url, session, width, height, x, y
        )
        is True
    )

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_fullscreen_window(__setup):
    driver_url, session = __setup
    window_rectangle_before = synchronous.get_window_rectangle(driver_url, session)

    assert synchronous.fullscreen_window(driver_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")

    synchronous.maximize_window(driver_url, session)

    assert await asynchronous.fullscreen_window(driver_url, session) is True

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_minimize_window(__setup):
    driver_url, session = __setup
    window_rectangle_before = synchronous.get_window_rectangle(driver_url, session)

    assert synchronous.minimize_window(driver_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") < window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") < window_rectangle_before.get("width")

    synchronous.maximize_window(driver_url, session)

    assert await asynchronous.minimize_window(driver_url, session) is True

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") < window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") < window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_maximize_window_asynchronous(__setup):
    driver_url, session = __setup
    window_rectangle_before = synchronous.get_window_rectangle(driver_url, session)

    assert await asynchronous.maximize_window(driver_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
def test_maximize_window_synchronous(__setup):
    driver_url, session = __setup
    window_rectangle_before = synchronous.get_window_rectangle(driver_url, session)

    assert synchronous.maximize_window(driver_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_switch_to_window(__setup, window_type):
    driver_url, session = __setup

    synchronous.new_window(driver_url, session, window_type)
    handles = synchronous.get_window_handles(driver_url, session)
    sample_page = handles[0]
    new_page = handles[1]

    assert synchronous.switch_to_window(driver_url, session, handle=new_page) is True
    assert synchronous.get_title(driver_url, session) == ""
    synchronous.switch_to_window(driver_url, session, handle=sample_page) is True

    assert (
        await asynchronous.switch_to_window(driver_url, session, handle=new_page)
        is True
    )
    assert synchronous.get_title(driver_url, session) == ""


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_new_window(__setup, window_type):
    driver_url, session = __setup

    assert synchronous.new_window(driver_url, session, window_type) is not None
    import time

    time.sleep(3)
    assert await asynchronous.new_window(driver_url, session, window_type) is not None


@mark.asyncio
async def test_switch_to_parent_frame_asynchronous(__setup):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver_url, session, locator_type, locator_value
    )
    assert (
        await asynchronous.switch_to_parent_frame(driver_url, session, element_frame)
        is True
    )


def test_switch_to_parent_frame_synchronous(__setup):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver_url, session, locator_type, locator_value
    )
    assert (
        synchronous.switch_to_parent_frame(driver_url, session, element_frame) is True
    )


@mark.asyncio
async def test_switch_to_frame_asynchronous(__setup):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver_url, session, locator_type, locator_value
    )
    assert (
        await asynchronous.switch_to_frame(driver_url, session, element_frame) is True
    )


def test_switch_to_frame_synchronous(__setup):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver_url, session, locator_type, locator_value
    )
    assert synchronous.switch_to_frame(driver_url, session, element_frame) is True


@mark.asyncio
async def test_send_alert_text(__setup):
    driver_url, session = __setup
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button-prompt"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.click(driver_url, session, element)

    assert synchronous.send_alert_text(driver_url, session, text="any1") is True
    synchronous.accept_alert(driver_url, session) is True

    synchronous.click(driver_url, session, element)
    assert await asynchronous.send_alert_text(driver_url, session, "any2") is True
    synchronous.accept_alert(driver_url, session) is True


@mark.asyncio
async def test_accept_alert(__setup):
    driver_url, session = __setup
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.click(driver_url, session, element)

    assert synchronous.accept_alert(driver_url, session) is True

    synchronous.click(driver_url, session, element)
    assert await asynchronous.accept_alert(driver_url, session) is True


@mark.asyncio
async def test_dismiss_alert(__setup):
    driver_url, session = __setup
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.click(driver_url, session, element)

    assert synchronous.dismiss_alert(driver_url, session) is True

    synchronous.click(driver_url, session, element)
    assert await asynchronous.dismiss_alert(driver_url, session) is True


@mark.asyncio
async def test_take_screenshot_element(__setup):
    driver_url, session = __setup
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.take_screenshot_element(driver_url, session, element) is True
    assert (
        await asynchronous.take_screenshot_element(driver_url, session, element) is True
    )


@mark.asyncio
async def test_take_screenshot(__setup):
    driver_url, session = __setup

    assert synchronous.take_screenshot(driver_url, session) is True
    assert await asynchronous.take_screenshot(driver_url, session) is True


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_asynchronous(__setup):
    driver_url, session = __setup

    cookies_before = synchronous.get_cookies(driver_url, session)

    response = await asynchronous.delete_all_cookies(driver_url, session)
    assert response is True

    cookies_after = synchronous.get_cookies(driver_url, session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_synchronous(__setup):
    driver_url, session = __setup

    cookies_before = synchronous.get_cookies(driver_url, session)

    assert synchronous.delete_all_cookies(driver_url, session) is True

    cookies_after = synchronous.get_cookies(driver_url, session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just with Firefox")
@mark.asyncio
async def test_get_named_cookie(__setup):
    driver_url, session = __setup
    name = "username"  # cookie created on page load
    expected = "John Doe"

    assert (
        synchronous.get_named_cookie(driver_url, session, name).get("value") == expected
    )
    response = await asynchronous.get_named_cookie(driver_url, session, name)
    assert response.get("value") == expected


@mark.asyncio
async def test_get_computed_label(__setup):
    driver_url, session = __setup
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "alert"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.get_computed_label(driver_url, session, element) == expected

    assert (
        await asynchronous.get_computed_label(driver_url, session, element) == expected
    )


@mark.asyncio
async def test_get_computed_role(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "textbox"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.get_computed_role(driver_url, session, element) == expected

    assert (
        await asynchronous.get_computed_role(driver_url, session, element) == expected
    )


@mark.asyncio
async def test_get_tag_name(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.get_tag_name(driver_url, session, element) == expected

    assert await asynchronous.get_tag_name(driver_url, session, element) == expected


@mark.parametrize(
    "locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")]
)
@mark.asyncio
async def test_find_element_from_shadow_root(__setup, locator, value):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    shadow_root = synchronous.get_shadow_root(driver_url, session, element)

    actual = synchronous.find_child_element(
        driver_url, session, shadow_root, locator, value
    )

    assert actual is not None

    actual = await asynchronous.find_child_element(
        driver_url, session, shadow_root, locator, value
    )

    assert actual is not None


@mark.parametrize(
    "locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")]
)
@mark.asyncio
async def test_find_elements_from_shadow_root(__setup, locator, value):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "shadow-root"
    one = 1

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    shadow_root = synchronous.get_shadow_root(driver_url, session, element)

    actual = synchronous.find_children_elements(
        driver_url, session, shadow_root, locator, value
    )

    assert len(actual) == one

    actual = await asynchronous.find_children_elements(
        driver_url, session, shadow_root, locator, value
    )

    assert len(actual) == one


@mark.asyncio
async def test_get_shadow_root(__setup):
    driver_url, session = __setup
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.get_shadow_root(driver_url, session, element) is not None

    response = await asynchronous.get_shadow_root(driver_url, session, element)
    assert response is not None


@mark.asyncio
async def test_get_rect(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//input"
    expected = {"height": 21, "width": 185, "x": 8, "y": 100.4375}

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.get_rect(driver_url, session, element) == expected

    assert await asynchronous.get_rect(driver_url, session, element) == expected


@mark.asyncio
async def test_move_to_element(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    assert synchronous.actions_move_to_element(driver_url, session, element) is True
    assert (
        await asynchronous.actions_move_to_element(driver_url, session, element) is True
    )


@mark.asyncio
async def test_actions_scroll_to_element(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    assert synchronous.actions_scroll_to_element(driver_url, session, element) is True
    assert (
        await asynchronous.actions_scroll_to_element(driver_url, session, element)
        is True
    )


@mark.asyncio
async def test_submit(__setup):
    driver_url, session = __setup
    locator_type = By.NAME
    locator_value = "my-form"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    assert synchronous.submit(driver_url, session, element) is True

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    assert await asynchronous.submit(driver_url, session, element) is True


@mark.asyncio
async def test_actions_click(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    assert synchronous.actions_click(driver_url, session, element) is True
    assert await asynchronous.actions_click(driver_url, session, element) is True


@mark.asyncio
async def test_raise_exception_when_element_not_found(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//invalid-tag"

    with raises(WebDriverError):
        synchronous.find_element(driver_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(
            driver_url, session, locator_type, locator_value
        )


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
    expected = 1  # parent inclusive
    locator_type = By.XPATH
    locator_value = "//div"

    parent_element = synchronous.find_element(
        driver_url, session, locator_type, '//div[@class="parent"]'
    )

    children_elements = synchronous.find_children_elements(
        driver_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected

    children_elements = await asynchronous.find_children_elements(
        driver_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected


@mark.asyncio
async def test_find_child_element(__setup):
    driver_url, session = __setup
    expected = "any4"
    locator_type = By.XPATH
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
    locator_type = By.CSS_SELECTOR
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
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)
    synchronous.send_keys(driver_url, session, element, "any")

    assert synchronous.get_active_element(driver_url, session) == element
    assert await asynchronous.get_active_element(driver_url, session) == element


@mark.asyncio
async def test_clear_element_fails_when_invalid_inputs(__setup):
    driver_url, session = __setup
    text = "any"
    element = "invalid"

    with raises(WebDriverError):
        synchronous.clear_element(driver_url, session, element) is True

    with raises(WebDriverError):
        await asynchronous.clear_element(driver_url, session, element)


@mark.asyncio
async def test_clear_element(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
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
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert synchronous.is_element_enabled(driver_url, session, element) is True
    assert await asynchronous.is_element_enabled(driver_url, session, element) is True


@mark.asyncio
async def test_get_css_value(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
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
    locator_type = By.XPATH
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
async def test_get_attribute_fails_when_invalid_attribute(__setup):
    driver_url, session = __setup
    attribute = "href"
    element = "invalid"

    with raises(WebDriverError):
        synchronous.get_attribute(driver_url, session, element, attribute)

    with raises(WebDriverError):
        await asynchronous.get_attribute(driver_url, session, element, attribute)


@mark.asyncio
async def test_get_attribute(__setup):
    driver_url, session = __setup
    attribute = "href"
    element = synchronous.find_element(driver_url, session, By.XPATH, "//a[@id='a1']")

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
    title = ""

    assert synchronous.go_back(driver_url, session) is True
    assert synchronous.get_title(driver_url, session) == title

    synchronous.go_forward(driver_url, session)
    assert await asynchronous.go_back(driver_url, session) is True
    assert synchronous.get_title(driver_url, session) == title


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
async def test_find_elements_fails_when_invalid_data_input(__setup):
    driver_url, session = __setup
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_elements(driver_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_elements(
            driver_url, session, locator_type, locator_value
        )


@mark.asyncio
async def test_find_elements(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
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
async def test_find_element_fails_when_invalid_data_input(__setup):
    driver_url, session = __setup
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_element(driver_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(
            driver_url, session, locator_type, locator_value
        )


@mark.asyncio
async def test_find_element(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
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
    locator_type = By.XPATH
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
    locator_type = By.XPATH
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.get_text(driver_url, session, element) == expected
    assert synchronous.get_text(driver_url, session, element) == expected


@mark.asyncio
async def test_send_keys(__setup):
    driver_url, session = __setup
    text_async = "any_async"
    text_sync = "any_sync"
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert (
        await asynchronous.send_keys(driver_url, session, element, text_async) is True
    )
    assert synchronous.send_keys(driver_url, session, element, text_sync) is True


@mark.asyncio
async def test_click(__setup):
    driver_url, session = __setup
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(driver_url, session, locator_type, locator_value)

    assert await asynchronous.click(driver_url, session, element) is True
    assert synchronous.click(driver_url, session, element) is True
