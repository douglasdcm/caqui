from pytest import mark, raises
from caqui import asynchronous, synchronous
from caqui.exceptions import WebDriverError
from caqui.by import By
from tests.constants import COOKIE


@mark.asyncio
async def test_add_cookie(setup_functional_environment):
    server_url, session = setup_functional_environment
    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    synchronous.go_to_page(
        server_url,
        session,
        "https://example.org/",
    )
    cookie = COOKIE
    assert synchronous.add_cookie(server_url, session, cookie) is True
    cookies_after = synchronous.get_cookies(server_url, session)
    assert len(cookies_after) > 0

    cookies_before = cookies_after
    cookie = cookies_before[0]
    cookie[By.NAME] = "another"

    assert await asynchronous.add_cookie(server_url, session, cookie) is True
    cookies_after = synchronous.get_cookies(server_url, session)
    assert len(cookies_after) > len(cookies_before)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookie_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    cookies = synchronous.get_cookies(server_url, session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert await asynchronous.delete_cookie(server_url, session, name) is True
    cookies = synchronous.get_cookies(server_url, session)
    assert len(cookies) == zero


@mark.skip(reason="works just in firefox")
@mark.asyncio
def test_delete_cookie_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    cookies = synchronous.get_cookies(server_url, session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert synchronous.delete_cookie(server_url, session, name) is True
    cookies = synchronous.get_cookies(server_url, session)
    assert len(cookies) == zero


@mark.asyncio
async def test_refresh_page(setup_functional_environment):
    server_url, session = setup_functional_environment

    element_before = synchronous.find_element(server_url, session, By.XPATH, "//input")
    assert (
        synchronous.refresh_page(
            server_url,
            session,
        )
        is True
    )

    element_after = synchronous.find_element(server_url, session, By.XPATH, "//input")
    assert element_before != element_after

    element_before = element_after
    assert await asynchronous.refresh_page(server_url, session) is True

    element_after = synchronous.find_element(server_url, session, By.XPATH, "//input")
    assert element_before != element_after


@mark.asyncio
async def test_go_forward(setup_functional_environment):
    server_url, session = setup_functional_environment
    title = "Sample page"

    synchronous.go_back(server_url, session)
    assert (
        synchronous.go_forward(
            server_url,
            session,
        )
        is True
    )
    assert synchronous.get_title(server_url, session) == title

    synchronous.go_back(server_url, session)
    assert await asynchronous.go_forward(server_url, session) is True
    assert synchronous.get_title(server_url, session) == title


@mark.asyncio
async def test_set_window_rectangle(setup_functional_environment):
    server_url, session = setup_functional_environment
    width = 500
    height = 300
    window_rectangle_before = synchronous.get_window_rectangle(server_url, session)
    x = window_rectangle_before.get("x") + 1
    y = window_rectangle_before.get("y") + 1

    assert synchronous.set_window_rectangle(server_url, session, width, height, x, y) is True

    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")

    synchronous.maximize_window(server_url, session)

    assert await asynchronous.set_window_rectangle(server_url, session, width, height, x, y) is True

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_fullscreen_window(setup_functional_environment):
    server_url, session = setup_functional_environment
    window_rectangle_before = synchronous.get_window_rectangle(server_url, session)

    assert synchronous.fullscreen_window(server_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")

    synchronous.maximize_window(server_url, session)

    assert await asynchronous.fullscreen_window(server_url, session) is True

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_minimize_window(setup_functional_environment):
    server_url, session = setup_functional_environment
    window_rectangle_before = synchronous.get_window_rectangle(server_url, session)

    assert synchronous.minimize_window(server_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") < window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") < window_rectangle_before.get("width")

    synchronous.maximize_window(server_url, session)

    assert await asynchronous.minimize_window(server_url, session) is True

    window_rectangle_after = None
    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") < window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") < window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_maximize_window_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    window_rectangle_before = synchronous.get_window_rectangle(server_url, session)

    assert await asynchronous.maximize_window(server_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
def test_maximize_window_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    window_rectangle_before = synchronous.get_window_rectangle(server_url, session)

    assert synchronous.maximize_window(server_url, session) is True

    window_rectangle_after = synchronous.get_window_rectangle(server_url, session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") > window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") > window_rectangle_before.get("width")


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_switch_to_window(setup_functional_environment, window_type):
    server_url, session = setup_functional_environment

    synchronous.new_window(server_url, session, window_type)
    handles = synchronous.get_window_handles(server_url, session)
    sample_page = handles[0]
    new_page = handles[1]

    assert synchronous.switch_to_window(server_url, session, handle=new_page) is True
    assert synchronous.get_title(server_url, session) == ""
    synchronous.switch_to_window(server_url, session, handle=sample_page) is True

    assert await asynchronous.switch_to_window(server_url, session, handle=new_page) is True
    assert synchronous.get_title(server_url, session) == ""


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_new_window(setup_functional_environment, window_type):
    server_url, session = setup_functional_environment

    assert synchronous.new_window(server_url, session, window_type) is not None
    import time

    time.sleep(3)
    assert await asynchronous.new_window(server_url, session, window_type) is not None


@mark.asyncio
async def test_switch_to_parent_frame_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert await asynchronous.switch_to_parent_frame(server_url, session, element_frame) is True


def test_switch_to_parent_frame_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.switch_to_parent_frame(server_url, session, element_frame) is True


@mark.asyncio
async def test_switch_to_frame_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert await asynchronous.switch_to_frame(server_url, session, element_frame) is True


def test_switch_to_frame_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.switch_to_frame(server_url, session, element_frame) is True


@mark.asyncio
async def test_send_alert_text(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button-prompt"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.click(server_url, session, element)

    assert synchronous.send_alert_text(server_url, session, text="any1") is True
    synchronous.accept_alert(server_url, session) is True

    synchronous.click(server_url, session, element)
    assert await asynchronous.send_alert_text(server_url, session, "any2") is True
    synchronous.accept_alert(server_url, session) is True


@mark.asyncio
async def test_accept_alert(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.click(server_url, session, element)

    assert synchronous.accept_alert(server_url, session) is True

    synchronous.click(server_url, session, element)
    assert await asynchronous.accept_alert(server_url, session) is True


@mark.asyncio
async def test_dismiss_alert(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.click(server_url, session, element)

    assert synchronous.dismiss_alert(server_url, session) is True

    synchronous.click(server_url, session, element)
    assert await asynchronous.dismiss_alert(server_url, session) is True


@mark.asyncio
async def test_take_screenshot_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.take_screenshot_element(server_url, session, element) is True
    assert await asynchronous.take_screenshot_element(server_url, session, element) is True


@mark.asyncio
async def test_take_screenshot(setup_functional_environment):
    server_url, session = setup_functional_environment

    assert synchronous.take_screenshot(server_url, session) is True
    assert await asynchronous.take_screenshot(server_url, session) is True


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment

    cookies_before = synchronous.get_cookies(server_url, session)

    response = await asynchronous.delete_all_cookies(server_url, session)
    assert response is True

    cookies_after = synchronous.get_cookies(server_url, session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment

    cookies_before = synchronous.get_cookies(server_url, session)

    assert synchronous.delete_all_cookies(server_url, session) is True

    cookies_after = synchronous.get_cookies(server_url, session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just with Firefox")
@mark.asyncio
async def test_get_named_cookie(setup_functional_environment):
    server_url, session = setup_functional_environment
    name = "username"  # cookie created on page load
    expected = "John Doe"

    assert synchronous.get_named_cookie(server_url, session, name).get("value") == expected
    response = await asynchronous.get_named_cookie(server_url, session, name)
    assert response.get("value") == expected


@mark.asyncio
async def test_get_computed_label(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "alert"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_computed_label(server_url, session, element) == expected

    assert await asynchronous.get_computed_label(server_url, session, element) == expected


@mark.asyncio
async def test_get_computed_role(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "textbox"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_computed_role(server_url, session, element) == expected

    assert await asynchronous.get_computed_role(server_url, session, element) == expected


@mark.asyncio
async def test_get_tag_name(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "input"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_tag_name(server_url, session, element) == expected

    assert await asynchronous.get_tag_name(server_url, session, element) == expected


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_element_from_shadow_root(setup_functional_environment, locator, value):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    shadow_root = synchronous.get_shadow_root(server_url, session, element)

    actual = synchronous.find_child_element(server_url, session, shadow_root, locator, value)

    assert actual is not None

    actual = await asynchronous.find_child_element(server_url, session, shadow_root, locator, value)

    assert actual is not None


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_elements_from_shadow_root(setup_functional_environment, locator, value):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "shadow-root"
    one = 1

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    shadow_root = synchronous.get_shadow_root(server_url, session, element)

    actual = synchronous.find_children_elements(server_url, session, shadow_root, locator, value)

    assert len(actual) == one

    actual = await asynchronous.find_children_elements(
        server_url, session, shadow_root, locator, value
    )

    assert len(actual) == one


@mark.asyncio
async def test_get_shadow_root(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_shadow_root(server_url, session, element) is not None

    response = await asynchronous.get_shadow_root(server_url, session, element)
    assert response is not None


@mark.asyncio
async def test_get_rect(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"
    expected = {"height": 21, "width": 185, "x": 8, "y": 100.4375}

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_rect(server_url, session, element) == expected

    assert await asynchronous.get_rect(server_url, session, element) == expected


@mark.asyncio
async def test_move_to_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.actions_move_to_element(server_url, session, element) is True
    assert await asynchronous.actions_move_to_element(server_url, session, element) is True


@mark.asyncio
async def test_actions_scroll_to_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.actions_scroll_to_element(server_url, session, element) is True
    assert await asynchronous.actions_scroll_to_element(server_url, session, element) is True


@mark.asyncio
async def test_submit(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.NAME
    locator_value = "my-form"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.submit(server_url, session, element) is True

    synchronous.refresh_page(server_url, session)
    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert await asynchronous.submit(server_url, session, element) is True


@mark.asyncio
async def test_actions_click(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    assert synchronous.actions_click(server_url, session, element) is True
    assert await asynchronous.actions_click(server_url, session, element) is True


@mark.asyncio
async def test_raise_exception_when_element_not_found(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//invalid-tag"

    with raises(WebDriverError):
        synchronous.find_element(server_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(server_url, session, locator_type, locator_value)


@mark.asyncio
async def test_set_timeouts(setup_functional_environment):
    server_url, session = setup_functional_environment
    timeouts_1 = 5000  # milliseconds
    timeouts_2 = 3000  # milliseconds

    synchronous.set_timeouts(server_url, session, timeouts_1)

    assert synchronous.get_timeouts(server_url, session).get("implicit") == timeouts_1

    await asynchronous.set_timeouts(server_url, session, timeouts_2)

    assert synchronous.get_timeouts(server_url, session).get("implicit") == timeouts_2


@mark.asyncio
async def test_find_children_elements(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = 1  # parent inclusive
    locator_type = By.XPATH
    locator_value = "//div"

    parent_element = synchronous.find_element(
        server_url, session, locator_type, '//div[@class="parent"]'
    )

    children_elements = synchronous.find_children_elements(
        server_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected

    children_elements = await asynchronous.find_children_elements(
        server_url, session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected


@mark.asyncio
async def test_find_child_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "any4"
    locator_type = By.XPATH
    locator_value = '//div[@class="child4"]'

    parent_element = synchronous.find_element(
        server_url, session, locator_type, '//div[@class="parent"]'
    )

    child_element = synchronous.find_child_element(
        server_url, session, parent_element, locator_type, locator_value
    )

    text = synchronous.get_text(server_url, session, child_element)

    assert text == expected
    child_element = await asynchronous.find_child_element(
        server_url, session, parent_element, locator_type, locator_value
    )
    text = synchronous.get_text(server_url, session, child_element)
    assert text == expected


@mark.asyncio
async def test_get_page_source(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "Sample page"

    assert expected in synchronous.get_page_source(server_url, session)
    assert expected in await asynchronous.get_page_source(server_url, session)


@mark.asyncio
async def test_execute_script_asynchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    script = "alert('any warn')"

    assert await asynchronous.execute_script(server_url, session, script) is None


def test_execute_script_synchronous(setup_functional_environment):
    server_url, session = setup_functional_environment
    script = "alert('any warn')"

    assert synchronous.execute_script(server_url, session, script) is None


@mark.asyncio
async def test_get_alert_text(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "any warn"

    alert_button = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.click(server_url, session, alert_button)

    assert synchronous.get_alert_text(server_url, session) == expected
    assert await asynchronous.get_alert_text(server_url, session) == expected


@mark.asyncio
async def test_get_active_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.send_keys(server_url, session, element, "any")

    assert synchronous.get_active_element(server_url, session) == element
    assert await asynchronous.get_active_element(server_url, session) == element


@mark.asyncio
async def test_clear_element_fails_when_invalid_inputs(setup_functional_environment):
    server_url, session = setup_functional_environment
    element = "invalid"

    with raises(WebDriverError):
        synchronous.clear_element(server_url, session, element) is True

    with raises(WebDriverError):
        await asynchronous.clear_element(server_url, session, element)


@mark.asyncio
async def test_clear_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"
    text = "any"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.send_keys(server_url, session, element, text)
    assert synchronous.clear_element(server_url, session, element) is True

    synchronous.send_keys(server_url, session, element, text)
    assert await asynchronous.clear_element(server_url, session, element) is True


@mark.asyncio
async def test_is_element_enabled(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.is_element_enabled(server_url, session, element) is True
    assert await asynchronous.is_element_enabled(server_url, session, element) is True


@mark.asyncio
async def test_get_css_value(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"
    property_name = "color"
    expected = "rgba(0, 0, 0, 1)"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.get_css_value(server_url, session, element, property_name) == expected
    assert await asynchronous.get_css_value(server_url, session, element, property_name) == expected


@mark.asyncio
async def test_is_element_selected(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert synchronous.is_element_selected(server_url, session, element) is False
    assert await asynchronous.is_element_selected(server_url, session, element) is False


@mark.asyncio
async def test_get_window_rectangle(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "height"

    assert expected in synchronous.get_window_rectangle(server_url, session)
    rectangle = await asynchronous.get_window_rectangle(server_url, session)
    assert expected in rectangle


@mark.asyncio
async def test_get_window_handles(setup_functional_environment):
    server_url, session = setup_functional_environment

    assert isinstance(synchronous.get_window_handles(server_url, session), list)
    handles = await asynchronous.get_window_handles(server_url, session)
    assert isinstance(handles, list)


def test_close_window_sync(setup_functional_environment):
    server_url, session = setup_functional_environment
    assert isinstance(synchronous.close_window(server_url, session), list)


@mark.asyncio
async def test_close_window_async(setup_functional_environment):
    server_url, session = setup_functional_environment

    response = await asynchronous.close_window(server_url, session)
    assert isinstance(response, list)


@mark.asyncio
async def test_get_window(setup_functional_environment):
    server_url, session = setup_functional_environment

    assert synchronous.get_window(server_url, session) is not None
    assert await asynchronous.get_window(server_url, session) is not None


@mark.asyncio
async def test_get_attribute_fails_when_invalid_attribute(setup_functional_environment):
    server_url, session = setup_functional_environment
    attribute = "href"
    element = "invalid"

    with raises(WebDriverError):
        synchronous.get_attribute(server_url, session, element, attribute)

    with raises(WebDriverError):
        await asynchronous.get_attribute(server_url, session, element, attribute)


@mark.asyncio
async def test_get_attribute(setup_functional_environment):
    server_url, session = setup_functional_environment
    attribute = "href"
    element = synchronous.find_element(server_url, session, By.XPATH, "//a[@id='a1']")

    assert synchronous.get_attribute(server_url, session, element, attribute) == "http://any1.com/"
    assert (
        await asynchronous.get_attribute(server_url, session, element, attribute)
        == "http://any1.com/"
    )


@mark.asyncio
async def test_get_cookies(setup_functional_environment):
    server_url, session = setup_functional_environment
    assert isinstance(synchronous.get_cookies(server_url, session), list)
    cookies = await asynchronous.get_cookies(server_url, session)
    assert isinstance(cookies, list)


@mark.asyncio
async def test_go_back(setup_functional_environment):
    server_url, session = setup_functional_environment
    title = ""

    assert synchronous.go_back(server_url, session) is True
    assert synchronous.get_title(server_url, session) == title

    synchronous.go_forward(server_url, session)
    assert await asynchronous.go_back(server_url, session) is True
    assert synchronous.get_title(server_url, session) == title


@mark.asyncio
async def test_get_url(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "playground.html"

    assert expected in synchronous.get_url(server_url, session)
    assert expected in await asynchronous.get_url(server_url, session)


@mark.asyncio
async def test_get_timeouts(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "implicit"

    assert expected in synchronous.get_timeouts(server_url, session)
    assert expected in await asynchronous.get_timeouts(server_url, session)


@mark.asyncio
async def test_get_status(setup_functional_environment):
    server_url, _ = setup_functional_environment
    expected = "ready"
    assert expected in synchronous.get_status(server_url).get("value")
    response = await asynchronous.get_status(server_url)
    assert expected in response.get("value")


@mark.asyncio
async def test_get_title(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "Sample page"

    assert synchronous.get_title(server_url, session) == expected
    assert await asynchronous.get_title(server_url, session) == expected


@mark.asyncio
async def test_find_elements_fails_when_invalid_data_input(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_elements(server_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_elements(server_url, session, locator_type, locator_value)


@mark.asyncio
async def test_find_elements(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"

    elements = synchronous.find_elements(server_url, session, locator_type, locator_value)
    async_elements = await asynchronous.find_elements(
        server_url, session, locator_type, locator_value
    )

    assert len(elements) > 0
    assert len(async_elements) > 0


@mark.asyncio
async def test_find_element_fails_when_invalid_data_input(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_element(server_url, session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(server_url, session, locator_type, locator_value)


@mark.asyncio
async def test_find_element(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//input"

    assert synchronous.find_element(server_url, session, locator_type, locator_value) is not None
    assert (
        await asynchronous.find_element(server_url, session, locator_type, locator_value)
        is not None
    )


@mark.asyncio
async def test_get_property(setup_functional_environment):
    server_url, session = setup_functional_environment
    text = "any_value"
    locator_type = By.XPATH
    locator_value = "//input"
    property = "value"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)
    synchronous.send_keys(server_url, session, element, text)

    assert synchronous.get_property(server_url, session, element, property) == text
    assert await asynchronous.get_property(server_url, session, element, property) == text


@mark.asyncio
async def test_get_text(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "end"
    locator_type = By.XPATH
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert await asynchronous.get_text(server_url, session, element) == expected
    assert synchronous.get_text(server_url, session, element) == expected


@mark.asyncio
async def test_send_keys(setup_functional_environment):
    server_url, session = setup_functional_environment
    text_async = "any_async"
    text_sync = "any_sync"
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert await asynchronous.send_keys(server_url, session, element, text_async) is True
    assert synchronous.send_keys(server_url, session, element, text_sync) is True


@mark.asyncio
async def test_click(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(server_url, session, locator_type, locator_value)

    assert await asynchronous.click(server_url, session, element) is True
    assert synchronous.click(server_url, session, element) is True
