import aiohttp
from pytest import mark, raises

from caqui import asynchronous, synchronous
from caqui.by import By
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE


@mark.asyncio
async def test_add_cookie(setup_playground):
    driver = setup_playground
    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    synchronous.go_to_page(
        driver.server_url,
        driver.session,
        "https://example.org/",
    )
    cookie = COOKIE
    assert synchronous.add_cookie(driver.server_url, driver.session, cookie) is True
    cookies_after = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies_after) > 0

    cookies_before = cookies_after
    cookie = cookies_before[0]
    cookie[By.NAME] = "another"

    assert await asynchronous.add_cookie(driver.server_url, driver.session, cookie) is True
    cookies_after = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies_after) > len(cookies_before)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookie_asynchronous(setup_playground):
    driver = setup_playground
    cookies = synchronous.get_cookies(driver.server_url, driver.session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert await asynchronous.delete_cookie(driver.server_url, driver.session, name) is True
    cookies = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies) == zero


@mark.skip(reason="works just in firefox")
@mark.asyncio
def test_delete_cookie_synchronous(setup_playground):
    driver = setup_playground
    cookies = synchronous.get_cookies(driver.server_url, driver.session)
    name = cookies[0].get(By.NAME)
    zero = 0

    assert synchronous.delete_cookie(driver.server_url, driver.session, name) is True
    cookies = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies) == zero


@mark.asyncio
async def test_refresh_page(setup_playground):
    driver = setup_playground

    element_before = synchronous.find_element(
        driver.server_url, driver.session, By.XPATH, "//input"
    )
    assert (
        synchronous.refresh_page(
            driver.server_url,
            driver.session,
        )
        is True
    )

    element_after = synchronous.find_element(driver.server_url, driver.session, By.XPATH, "//input")
    assert element_before != element_after

    element_before = element_after
    assert await asynchronous.refresh_page(driver.server_url, driver.session) is True

    element_after = synchronous.find_element(driver.server_url, driver.session, By.XPATH, "//input")
    assert element_before != element_after


@mark.asyncio
async def test_go_forward(setup_playground):
    driver = setup_playground
    title = "Sample page"

    synchronous.go_back(driver.server_url, driver.session)
    assert (
        synchronous.go_forward(
            driver.server_url,
            driver.session,
        )
        is True
    )
    assert synchronous.get_title(driver.server_url, driver.session) == title

    synchronous.go_back(driver.server_url, driver.session)
    assert await asynchronous.go_forward(driver.server_url, driver.session) is True
    assert synchronous.get_title(driver.server_url, driver.session) == title


@mark.asyncio
async def test_set_window_rectangle(setup_playground):
    driver = setup_playground
    width = 500
    height = 300
    window_rectangle_before = synchronous.get_window_rectangle(driver.server_url, driver.session)
    x = window_rectangle_before.get("x", 0) + 1
    y = window_rectangle_before.get("y", 0) + 1

    assert (
        synchronous.set_window_rectangle(driver.server_url, driver.session, width, height, x, y)
        is True
    )

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")

    synchronous.maximize_window(driver.server_url, driver.session)

    assert (
        await asynchronous.set_window_rectangle(
            driver.server_url, driver.session, width, height, x, y
        )
        is True
    )

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")
    assert window_rectangle_after.get("x") != window_rectangle_before.get("x")
    assert window_rectangle_after.get("y") != window_rectangle_before.get("y")


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_fullscreen_window(setup_playground):
    driver = setup_playground
    window_rectangle_before = synchronous.get_window_rectangle(driver.server_url, driver.session)

    assert synchronous.fullscreen_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) > window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) > window_rectangle_before.get("width", 0)

    synchronous.maximize_window(driver.server_url, driver.session)

    assert await asynchronous.fullscreen_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) > window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) > window_rectangle_before.get("width", 0)


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_minimize_window(setup_playground):
    driver = setup_playground
    window_rectangle_before = synchronous.get_window_rectangle(driver.server_url, driver.session)

    assert synchronous.minimize_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) < window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) < window_rectangle_before.get("width", 0)

    synchronous.maximize_window(driver.server_url, driver.session)

    assert await asynchronous.minimize_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) < window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) < window_rectangle_before.get("width", 0)


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
async def test_maximize_window_asynchronous(setup_playground):
    driver = setup_playground
    window_rectangle_before = synchronous.get_window_rectangle(driver.server_url, driver.session)

    assert await asynchronous.maximize_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) > window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) > window_rectangle_before.get("width", 0)


@mark.skip(reason="does not work in headless mode")
@mark.asyncio
def test_maximize_window_synchronous(setup_playground):
    driver = setup_playground
    window_rectangle_before = synchronous.get_window_rectangle(driver.server_url, driver.session)

    assert synchronous.maximize_window(driver.server_url, driver.session) is True

    window_rectangle_after = synchronous.get_window_rectangle(driver.server_url, driver.session)
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height", 0) > window_rectangle_before.get("height", 0)
    assert window_rectangle_after.get("width", 0) > window_rectangle_before.get("width", 0)


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_switch_to_window(setup_playground, window_type):
    driver = setup_playground

    synchronous.new_window(driver.server_url, driver.session, window_type)
    handles = synchronous.get_window_handles(driver.server_url, driver.session)
    sample_page = handles[0]
    new_page = handles[1]

    assert synchronous.switch_to_window(driver.server_url, driver.session, handle=new_page) is True
    assert synchronous.get_title(driver.server_url, driver.session) == ""
    synchronous.switch_to_window(driver.server_url, driver.session, handle=sample_page) is True

    assert (
        await asynchronous.switch_to_window(driver.server_url, driver.session, handle=new_page)
        is True
    )
    assert synchronous.get_title(driver.server_url, driver.session) == ""


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_new_window(setup_playground, window_type):
    driver = setup_playground

    assert synchronous.new_window(driver.server_url, driver.session, window_type) is not None
    import time

    time.sleep(3)
    assert await asynchronous.new_window(driver.server_url, driver.session, window_type) is not None


@mark.asyncio
async def test_switch_to_parent_frame_asynchronous(setup_playground):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert (
        await asynchronous.switch_to_parent_frame(driver.server_url, driver.session, element_frame)
        is True
    )


def test_switch_to_parent_frame_synchronous(setup_playground):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert (
        synchronous.switch_to_parent_frame(driver.server_url, driver.session, element_frame) is True
    )


@mark.asyncio
async def test_switch_to_frame_asynchronous(setup_playground):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert (
        await asynchronous.switch_to_frame(driver.server_url, driver.session, element_frame) is True
    )


def test_switch_to_frame_synchronous(setup_playground):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert synchronous.switch_to_frame(driver.server_url, driver.session, element_frame) is True


@mark.asyncio
async def test_send_alert_text(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button-prompt"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.click(driver.server_url, driver.session, element)

    assert synchronous.send_alert_text(driver.server_url, driver.session, text="any1") is True
    synchronous.accept_alert(driver.server_url, driver.session) is True

    synchronous.click(driver.server_url, driver.session, element)
    assert await asynchronous.send_alert_text(driver.server_url, driver.session, "any2") is True
    synchronous.accept_alert(driver.server_url, driver.session) is True


@mark.asyncio
async def test_accept_alert(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.click(driver.server_url, driver.session, element)

    assert synchronous.accept_alert(driver.server_url, driver.session) is True

    synchronous.click(driver.server_url, driver.session, element)
    assert await asynchronous.accept_alert(driver.server_url, driver.session) is True


@mark.asyncio
async def test_dismiss_alert(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.click(driver.server_url, driver.session, element)

    assert synchronous.dismiss_alert(driver.server_url, driver.session) is True

    synchronous.click(driver.server_url, driver.session, element)
    assert await asynchronous.dismiss_alert(driver.server_url, driver.session) is True


@mark.asyncio
async def test_take_screenshot_element(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.take_screenshot_element(driver.server_url, driver.session, element) is True
    async with aiohttp.ClientSession() as session_http:
        assert (
            await asynchronous.take_screenshot_element(
                driver.server_url, driver.session, element, session_http=session_http
            )
            is True
        )


@mark.asyncio
async def test_take_screenshot(setup_playground):
    driver = setup_playground

    assert synchronous.take_screenshot(driver.server_url, driver.session) is True
    assert await asynchronous.take_screenshot(driver.server_url, driver.session) is True


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_asynchronous(setup_playground):
    driver = setup_playground

    cookies_before = synchronous.get_cookies(driver.server_url, driver.session)

    response = await asynchronous.delete_all_cookies(driver.server_url, driver.session)
    assert response is True

    cookies_after = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_synchronous(setup_playground):
    driver = setup_playground

    cookies_before = synchronous.get_cookies(driver.server_url, driver.session)

    assert synchronous.delete_all_cookies(driver.server_url, driver.session) is True

    cookies_after = synchronous.get_cookies(driver.server_url, driver.session)
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just with Firefox")
@mark.asyncio
async def test_get_named_cookie(setup_playground):
    driver = setup_playground
    name = "username"  # cookie created on page load
    expected = "John Doe"

    assert (
        synchronous.get_named_cookie(driver.server_url, driver.session, name).get("value")
        == expected
    )
    response = await asynchronous.get_named_cookie(driver.server_url, driver.session, name)
    assert response == expected


@mark.asyncio
async def test_get_computed_label(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "alert"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.get_computed_label(driver.server_url, driver.session, element) == expected

    assert (
        await asynchronous.get_computed_label(driver.server_url, driver.session, element)
        == expected
    )


@mark.asyncio
async def test_get_computed_role(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "textbox"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.get_computed_role(driver.server_url, driver.session, element) == expected

    assert (
        await asynchronous.get_computed_role(driver.server_url, driver.session, element) == expected
    )


@mark.asyncio
async def test_get_tag_name(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "input"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.get_tag_name(driver.server_url, driver.session, element) == expected

    assert await asynchronous.get_tag_name(driver.server_url, driver.session, element) == expected


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_element_from_shadow_root(setup_playground, locator, value):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    shadow_root = synchronous.get_shadow_root(driver.server_url, driver.session, element)

    actual = synchronous.find_child_element(
        driver.server_url, driver.session, shadow_root, locator, value
    )

    assert actual is not None

    actual = await asynchronous.find_child_element(
        driver.server_url, driver.session, shadow_root, locator, value
    )

    assert actual is not None


@mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
@mark.asyncio
async def test_find_elements_from_shadow_root(setup_playground, locator, value):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "shadow-root"
    one = 1

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    shadow_root = synchronous.get_shadow_root(driver.server_url, driver.session, element)

    actual = synchronous.find_children_elements(
        driver.server_url, driver.session, shadow_root, locator, value
    )

    assert len(actual) == one

    actual = await asynchronous.find_children_elements(
        driver.server_url, driver.session, shadow_root, locator, value
    )

    assert len(actual) == one


@mark.asyncio
async def test_get_shadow_root(setup_playground):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "shadow-root"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.get_shadow_root(driver.server_url, driver.session, element) is not None

    response = await asynchronous.get_shadow_root(driver.server_url, driver.session, element)
    assert response is not None


@mark.asyncio
async def test_get_rect(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    expected = {"height": 21, "width": 185, "x": 8, "y": 100.4375}

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.get_rect(driver.server_url, driver.session, element) == expected

    assert await asynchronous.get_rect(driver.server_url, driver.session, element) == expected


@mark.asyncio
async def test_move_to_element(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert synchronous.actions_move_to_element(driver.server_url, driver.session, element) is True
    assert (
        await asynchronous.actions_move_to_element(driver.server_url, driver.session, element)
        is True
    )


@mark.asyncio
async def test_actions_scroll_to_element(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert synchronous.actions_scroll_to_element(driver.server_url, driver.session, element) is True
    assert (
        await asynchronous.actions_scroll_to_element(driver.server_url, driver.session, element)
        is True
    )


@mark.asyncio
async def test_submit(setup_playground):
    driver = setup_playground
    locator_type = By.NAME
    locator_value = "my-form"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert synchronous.submit(driver.server_url, driver.session, element) is True

    synchronous.refresh_page(driver.server_url, driver.session)
    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert await asynchronous.submit(driver.server_url, driver.session, element) is True


@mark.asyncio
async def test_actions_click(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    assert synchronous.actions_click(driver.server_url, driver.session, element) is True
    assert await asynchronous.actions_click(driver.server_url, driver.session, element) is True


@mark.asyncio
async def test_raise_exception_when_element_not_found(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//invalid-tag"

    with raises(WebDriverError):
        synchronous.find_element(driver.server_url, driver.session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(
            driver.server_url, driver.session, locator_type, locator_value
        )


@mark.asyncio
async def test_set_timeouts(setup_playground):
    driver = setup_playground
    timeouts_1 = 5000  # milliseconds
    timeouts_2 = 3000  # milliseconds

    synchronous.set_timeouts(driver.server_url, driver.session, timeouts_1)

    assert synchronous.get_timeouts(driver.server_url, driver.session).get("implicit") == timeouts_1

    await asynchronous.set_timeouts(driver.server_url, driver.session, timeouts_2)

    assert synchronous.get_timeouts(driver.server_url, driver.session).get("implicit") == timeouts_2


@mark.asyncio
async def test_find_children_elements(setup_playground):
    driver = setup_playground
    expected = 1  # parent inclusive
    locator_type = By.XPATH
    locator_value = "//div"

    parent_element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, '//div[@class="parent"]'
    )

    children_elements = synchronous.find_children_elements(
        driver.server_url, driver.session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected

    children_elements = await asynchronous.find_children_elements(
        driver.server_url, driver.session, parent_element, locator_type, locator_value
    )

    assert len(children_elements) > expected


@mark.asyncio
async def test_find_child_element(setup_playground):
    driver = setup_playground
    expected = "any4"
    locator_type = By.XPATH
    locator_value = '//div[@class="child4"]'

    parent_element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, '//div[@class="parent"]'
    )

    child_element = synchronous.find_child_element(
        driver.server_url, driver.session, parent_element, locator_type, locator_value
    )

    text = synchronous.get_text(driver.server_url, driver.session, child_element)

    assert text == expected
    child_element = await asynchronous.find_child_element(
        driver.server_url, driver.session, parent_element, locator_type, locator_value
    )
    text = synchronous.get_text(driver.server_url, driver.session, child_element)
    assert text == expected


@mark.asyncio
async def test_get_page_source(setup_playground):
    driver = setup_playground
    expected = "Sample page"

    assert expected in synchronous.get_page_source(driver.server_url, driver.session)
    assert expected in await asynchronous.get_page_source(driver.server_url, driver.session)


@mark.asyncio
async def test_execute_script_asynchronous(setup_playground):
    driver = setup_playground
    script = "alert('any warn')"

    assert await asynchronous.execute_script(driver.server_url, driver.session, script) is None


def test_execute_script_synchronous(setup_playground):
    driver = setup_playground
    script = "alert('any warn')"

    assert synchronous.execute_script(driver.server_url, driver.session, script) is None


@mark.asyncio
async def test_get_alert_text(setup_playground):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "any warn"

    alert_button = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.click(driver.server_url, driver.session, alert_button)

    assert synchronous.get_alert_text(driver.server_url, driver.session) == expected
    assert await asynchronous.get_alert_text(driver.server_url, driver.session) == expected


@mark.asyncio
async def test_get_active_element(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.send_keys(driver.server_url, driver.session, element, "any")

    assert synchronous.get_active_element(driver.server_url, driver.session) == element
    assert await asynchronous.get_active_element(driver.server_url, driver.session) == element


@mark.asyncio
async def test_clear_element_fails_when_invalid_inputs(setup_playground):
    driver = setup_playground
    element = "invalid"

    with raises(WebDriverError):
        synchronous.clear_element(driver.server_url, driver.session, element) is True

    with raises(WebDriverError):
        await asynchronous.clear_element(driver.server_url, driver.session, element)


@mark.asyncio
async def test_clear_element(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    text = "any"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.send_keys(driver.server_url, driver.session, element, text)
    assert synchronous.clear_element(driver.server_url, driver.session, element) is True

    synchronous.send_keys(driver.server_url, driver.session, element, text)
    assert await asynchronous.clear_element(driver.server_url, driver.session, element) is True


@mark.asyncio
async def test_is_element_enabled(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.is_element_enabled(driver.server_url, driver.session, element) is True
    assert await asynchronous.is_element_enabled(driver.server_url, driver.session, element) is True


@mark.asyncio
async def test_get_css_value(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    property_name = "color"
    expected = "rgba(0, 0, 0, 1)"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert (
        synchronous.get_css_value(driver.server_url, driver.session, element, property_name)
        == expected
    )
    assert (
        await asynchronous.get_css_value(driver.server_url, driver.session, element, property_name)
        == expected
    )


@mark.asyncio
async def test_is_element_selected(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert synchronous.is_element_selected(driver.server_url, driver.session, element) is False
    assert (
        await asynchronous.is_element_selected(driver.server_url, driver.session, element) is False
    )


@mark.asyncio
async def test_get_window_rectangle(setup_playground):
    driver = setup_playground
    expected = "height"

    assert expected in synchronous.get_window_rectangle(driver.server_url, driver.session)
    rectangle = await asynchronous.get_window_rectangle(driver.server_url, driver.session)
    assert expected in rectangle


@mark.asyncio
async def test_get_window_handles(setup_playground):
    driver = setup_playground

    assert isinstance(synchronous.get_window_handles(driver.server_url, driver.session), list)
    handles = await asynchronous.get_window_handles(driver.server_url, driver.session)
    assert isinstance(handles, list)


def test_close_window_sync(setup_playground):
    driver = setup_playground
    assert isinstance(synchronous.close_window(driver.server_url, driver.session), list)


@mark.asyncio
async def test_close_window_async(setup_playground):
    driver = setup_playground

    response = await asynchronous.close_window(driver.server_url, driver.session)
    assert isinstance(response, list)


@mark.asyncio
async def test_get_window(setup_playground):
    driver = setup_playground

    assert synchronous.get_window(driver.server_url, driver.session) is not None
    assert await asynchronous.get_window(driver.server_url, driver.session) is not None


@mark.asyncio
async def test_get_attribute_fails_when_invalid_attribute(setup_playground):
    driver = setup_playground
    attribute = "href"
    element = "invalid"

    with raises(WebDriverError):
        synchronous.get_attribute(driver.server_url, driver.session, element, attribute)

    with raises(WebDriverError):
        await asynchronous.get_attribute(driver.server_url, driver.session, element, attribute)


@mark.asyncio
async def test_get_attribute(setup_playground):
    driver = setup_playground
    attribute = "href"
    element = synchronous.find_element(driver.server_url, driver.session, By.XPATH, "//a[@id='a1']")

    assert (
        synchronous.get_attribute(driver.server_url, driver.session, element, attribute)
        == "http://any1.com/"
    )
    assert (
        await asynchronous.get_attribute(driver.server_url, driver.session, element, attribute)
        == "http://any1.com/"
    )


@mark.asyncio
async def test_get_cookies(setup_playground):
    driver = setup_playground
    assert isinstance(synchronous.get_cookies(driver.server_url, driver.session), list)
    cookies = await asynchronous.get_cookies(driver.server_url, driver.session)
    assert isinstance(cookies, list)


@mark.asyncio
async def test_go_back(setup_playground):
    driver = setup_playground
    title = ""

    assert synchronous.go_back(driver.server_url, driver.session) is True
    assert synchronous.get_title(driver.server_url, driver.session) == title

    synchronous.go_forward(driver.server_url, driver.session)
    assert await asynchronous.go_back(driver.server_url, driver.session) is True
    assert synchronous.get_title(driver.server_url, driver.session) == title


@mark.asyncio
async def test_get_url(setup_playground):
    driver = setup_playground
    expected = "playground.html"

    assert expected in synchronous.get_url(driver.server_url, driver.session)
    assert expected in await asynchronous.get_url(driver.server_url, driver.session)


@mark.asyncio
async def test_get_timeouts(setup_playground):
    driver = setup_playground
    expected = "implicit"

    assert expected in synchronous.get_timeouts(driver.server_url, driver.session)
    assert expected in await asynchronous.get_timeouts(driver.server_url, driver.session)


@mark.asyncio
async def test_get_status(setup_playground):
    driver = setup_playground
    expected = "ready"
    assert expected in synchronous.get_status(driver.server_url).get("value", [])
    response = await asynchronous.get_status(driver.server_url)
    assert expected in response.get("value", [])


@mark.asyncio
async def test_get_title(setup_playground):
    driver = setup_playground
    expected = "Sample page"

    assert synchronous.get_title(driver.server_url, driver.session) == expected
    assert await asynchronous.get_title(driver.server_url, driver.session) == expected


@mark.asyncio
async def test_find_elements_fails_when_invalid_data_input(
    setup_playground,
):
    driver = setup_playground
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_elements(driver.server_url, driver.session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_elements(
            driver.server_url, driver.session, locator_type, locator_value
        )


@mark.asyncio
async def test_find_elements(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    elements = synchronous.find_elements(
        driver.server_url, driver.session, locator_type, locator_value
    )
    async_elements = await asynchronous.find_elements(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert len(elements) > 0
    assert len(async_elements) > 0


@mark.asyncio
async def test_find_element_fails_when_invalid_data_input(setup_playground):
    driver = setup_playground
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        synchronous.find_element(driver.server_url, driver.session, locator_type, locator_value)

    with raises(WebDriverError):
        await asynchronous.find_element(
            driver.server_url, driver.session, locator_type, locator_value
        )


@mark.asyncio
async def test_find_element(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    assert (
        synchronous.find_element(driver.server_url, driver.session, locator_type, locator_value)
        is not None
    )
    assert (
        await asynchronous.find_element(
            driver.server_url, driver.session, locator_type, locator_value
        )
        is not None
    )


@mark.asyncio
async def test_get_property(setup_playground):
    driver = setup_playground
    text = "any_value"
    locator_type = By.XPATH
    locator_value = "//input"
    property = "value"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )
    synchronous.send_keys(driver.server_url, driver.session, element, text)

    assert synchronous.get_property(driver.server_url, driver.session, element, property) == text
    assert (
        await asynchronous.get_property(driver.server_url, driver.session, element, property)
        == text
    )


@mark.asyncio
async def test_get_text(setup_playground):
    driver = setup_playground
    expected = "end"
    locator_type = By.XPATH
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert await asynchronous.get_text(driver.server_url, driver.session, element) == expected
    assert synchronous.get_text(driver.server_url, driver.session, element) == expected


@mark.asyncio
async def test_send_keys(setup_playground):
    driver = setup_playground
    text_async = "any_async"
    text_sync = "any_sync"
    locator_type = By.XPATH
    locator_value = "//input"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert (
        await asynchronous.send_keys(driver.server_url, driver.session, element, text_async) is True
    )
    assert synchronous.send_keys(driver.server_url, driver.session, element, text_sync) is True


@mark.asyncio
async def test_click(setup_playground):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"

    element = synchronous.find_element(
        driver.server_url, driver.session, locator_type, locator_value
    )

    assert await asynchronous.click(driver.server_url, driver.session, element) is True
    assert synchronous.click(driver.server_url, driver.session, element) is True
