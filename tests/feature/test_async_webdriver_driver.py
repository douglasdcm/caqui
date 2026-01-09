from pytest import mark, raises

from caqui.by import By
from caqui.easy.drivers import AsyncDriver
from caqui.exceptions import WebDriverError


@mark.asyncio
async def test_refresh_page(setup_playground: AsyncDriver):
    driver = setup_playground
    element_before = await driver.find_element(By.XPATH, "//input")
    await driver.refresh()
    element_after = await driver.find_element(By.XPATH, "//input")
    assert element_before != element_after
    element_before = element_after
    await driver.refresh()
    element_after = await driver.find_element(By.XPATH, "//input")
    assert element_before != element_after
    element_after = await driver.find_element(By.XPATH, "//input")
    assert element_before != element_after


@mark.asyncio
async def test_go_forward(setup_playground: AsyncDriver):
    driver = setup_playground
    title = "Sample page"
    await driver.back()
    await driver.forward()
    assert driver.title == title


@mark.asyncio
async def test_set_window_rectangle(setup_playground: AsyncDriver):
    driver = setup_playground
    window_rectangle_before = await driver.get_window_size()
    x = window_rectangle_before.get("width", 0) + 1
    y = window_rectangle_before.get("height", 0) + 1
    await driver.set_window_size(width=x, height=y)
    window_rectangle_after = await driver.get_window_size()
    assert window_rectangle_after != window_rectangle_before
    assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
    assert window_rectangle_after.get("width") != window_rectangle_before.get("width")


@mark.asyncio
async def test_fullscreen_window(setup_playground: AsyncDriver):
    driver = setup_playground
    assert await driver.fullscreen_window() is None
    await driver.maximize_window()
    assert await driver.fullscreen_window() is None


@mark.asyncio
async def test_minimize_window(setup_playground: AsyncDriver):
    driver = setup_playground
    await driver.minimize_window()


@mark.asyncio
async def test_maximize_window_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground
    await driver.maximize_window()


@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_new_window(setup_playground: AsyncDriver, window_type):
    driver = setup_playground
    assert await driver.switch_to.new_window(window_type) is not None
    assert await driver.switch_to.new_window(window_type) is not None


@mark.asyncio
async def test_take_screenshot_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    element = await driver.find_element(locator_type, locator_value)
    await element.screenshot("/tmp/picture.png")


@mark.asyncio
async def test_take_screenshot(setup_playground: AsyncDriver):
    driver = setup_playground
    await driver.save_screenshot("/tmp/picture.png")


@mark.asyncio
async def test_get_computed_label(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "alert"
    element = await driver.find_element(locator_type, locator_value)
    assert await element.get_computed_label() == expected


@mark.asyncio
async def test_get_computed_role(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "textbox"
    element = await driver.find_element(locator_type, locator_value)
    assert await element.get_computed_role() == expected


@mark.asyncio
async def test_get_tag_name(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    expected = "input"
    element = await driver.find_element(locator_type, locator_value)
    assert await element.get_tag_name() == expected


@mark.asyncio
async def test_get_rect(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    element = await driver.find_element(locator_type, locator_value)
    actual = await element.get_rect()
    assert actual["height"]
    assert actual["width"]
    assert actual["x"]
    assert actual["y"]


@mark.asyncio
async def test_move_to_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"
    element = await driver.find_element(locator_type, locator_value)
    await driver.actions.move_to_element(element).perform()


@mark.asyncio
async def test_actions_scroll_to_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"
    element = await driver.find_element(locator_type, locator_value)
    await driver.actions.scroll_to_element(element).perform()


@mark.asyncio
async def test_submit_foo(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.NAME
    locator_value = "my-form"
    element = await driver.find_element(locator_type, locator_value)
    await element.submit()


@mark.asyncio
async def test_actions_click(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"
    element = await driver.find_element(locator_type, locator_value)
    await driver.actions.click(element).perform()


@mark.asyncio
async def test_raise_exception_when_element_not_found(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//invalid-tag"
    with raises(WebDriverError):
        await driver.find_element(locator_type, locator_value)


@mark.asyncio
async def test_find_children_elements(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = 1  # parent inclusive
    locator_type = By.XPATH
    locator_value = "//div"
    parent_element = await driver.find_element(locator_type, '//div[@class="parent"]')
    children_elements = await parent_element.find_elements(locator_type, locator_value)
    assert len(children_elements) > expected


@mark.asyncio
async def test_find_child_element(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "any4"
    locator_type = By.XPATH
    locator_value = '//div[@class="child4"]'
    parent_element = await driver.find_element(locator_type, '//div[@class="parent"]')
    child_element = await parent_element.find_element(locator_type, locator_value)
    text = await child_element.get_text()
    assert text == expected


@mark.asyncio
async def test_get_page_source(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "Sample page"
    assert expected in driver.page_source


@mark.asyncio
async def test_execute_script_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground
    script = "alert('any warn')"
    assert await driver.execute_script(script) is None


@mark.asyncio
async def test_get_alert_text(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"
    expected = "any warn"
    alert_button = await driver.find_element(locator_type, locator_value)
    await alert_button.click()
    assert driver.alert.text == expected


@mark.asyncio
async def test_get_active_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    locator_value = '//*[@id="button"]'
    element = await driver.find_element(locator_type, locator_value)
    await element.send_keys("any")
    assert driver.switch_to.active_element.text == element.text


@mark.asyncio
async def test_clear_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    text = "any"
    element = await driver.find_element(locator_type, locator_value)
    await element.send_keys(text)
    await element.clear()
