import time

from pytest import mark, raises

from caqui.cdp.asynchronous.drivers import AsyncDriverCDP
from caqui.cdp.by import By
from caqui.exceptions import WebDriverError


class TestCDPDriver:
    @mark.asyncio
    async def test_cdp_refresh_page(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground

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
    async def test_cdp_go_forward(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        title = "Sample page"
        await driver.back()
        await driver.forward()
        time.sleep(0.1)
        assert await driver.get_title() == title

    @mark.asyncio
    async def test_cdp_set_window_rectangle(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        window_rectangle_before = await driver.get_window_size()
        x = window_rectangle_before.get("width", 0) + 1
        y = window_rectangle_before.get("height", 0) + 1

        await driver.set_window_size(width=x, height=y)
        window_rectangle_after = await driver.get_window_size()

        assert window_rectangle_after != window_rectangle_before
        assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
        assert window_rectangle_after.get("width") != window_rectangle_before.get("width")

    @mark.asyncio
    async def test_cdp_fullscreen_window(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        window_rectangle_before = await driver.get_window_size()
        await driver.fullscreen_window()
        window_rectangle_after = await driver.get_window_size()
        assert window_rectangle_after != window_rectangle_before

    @mark.asyncio
    async def test_cdp_minimize_window(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        await driver.minimize_window()

    @mark.asyncio
    async def test_cdp_maximize_window_asynchronous(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        await driver.maximize_window()

    @mark.asyncio
    async def test_cdp_new_window(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        assert await driver.switch_to.new_window() is not None

    @mark.asyncio
    async def test_cdp_take_screenshot_element(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        element = await driver.find_element(locator_type, locator_value)
        await element.screenshot("/tmp/picture.png")

    @mark.asyncio
    async def test_cdp_take_screenshot(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        await driver.save_screenshot("/tmp/picture.png")

    @mark.asyncio
    async def test_cdp_get_computed_label(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        expected = "alert"

        element = await driver.find_element(locator_type, locator_value)

        assert await element.get_computed_label() == expected

    @mark.asyncio
    async def test_cdp_get_computed_role(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        expected = "textbox"

        element = await driver.find_element(locator_type, locator_value)

        assert await element.get_computed_role() == expected

    @mark.asyncio
    async def test_cdp_get_tag_name(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        expected = "INPUT"

        element = await driver.find_element(locator_type, locator_value)

        assert await element.get_tag_name() == expected

    @mark.asyncio
    async def test_cdp_get_rect(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"

        element = await driver.find_element(locator_type, locator_value)

        actual = await element.get_rect()
        assert actual["height"]
        assert actual["width"]
        assert actual["x"]
        assert actual["y"]

    @mark.asyncio
    async def test_cdp_move_to_element(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = await driver.find_element(locator_type, locator_value)
        await driver.actions.move_to_element(element).perform()

    @mark.asyncio
    async def test_cdp_actions_scroll_to_element(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = await driver.find_element(locator_type, locator_value)
        await driver.actions.scroll_to_element(element).perform()

    @mark.asyncio
    async def test_cdp_submit_foo(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.NAME
        locator_value = "my-form"

        element = await driver.find_element(locator_type, locator_value)
        await element.submit()

    @mark.asyncio
    async def test_cdp_actions_click(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = await driver.find_element(locator_type, locator_value)
        await driver.actions.click(element).perform()

    @mark.asyncio
    async def test_cdp_raise_exception_when_element_not_found(
        self, setup_cdp_playground: AsyncDriverCDP
    ):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//invalid-tag"

        with raises(WebDriverError):
            await driver.find_element(locator_type, locator_value)

    @mark.asyncio
    async def test_cdp_find_children_elements(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        expected = 1  # parent inclusive
        locator_type = By.XPATH
        locator_value = "//div"

        parent_element = await driver.find_element(locator_type, '//div[@class="parent"]')

        children_elements = await parent_element.find_elements(locator_type, locator_value)

        assert len(children_elements) > expected

    @mark.asyncio
    async def test_cdp_find_child_element(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        expected = "any4"
        locator_type = By.XPATH
        locator_value = '//div[@class="child4"]'

        parent_element = await driver.find_element(locator_type, '//div[@class="parent"]')
        child_element = await parent_element.find_element(locator_type, locator_value)
        text = await child_element.get_text()
        assert text == expected

    @mark.asyncio
    async def test_cdp_get_page_source(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        expected = "Sample page"

        assert expected in await driver.get_page_source()

    @mark.asyncio
    async def test_cdp_execute_script_asynchronous(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        script = "alert('any warn')"
        script = "style.background='#000000'"

        assert await driver.execute_script(script) is None

    @mark.asyncio
    async def test_cdp_get_alert_text(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        expected = "any warn"
        await driver.find_element(locator_type, locator_value)
        assert await driver.alert.get_text() == expected

    @mark.asyncio
    async def test_cdp_get_active_element(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        locator_value = '//*[@id="button"]'

        element = await driver.find_element(locator_type, locator_value)
        await element.send_keys("any")

        element = await driver.switch_to.get_active_element()
        assert await element.get_text() == await element.get_text()

    @mark.asyncio
    async def test_cdp_clear_element_foo(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        text = "any"

        element = await driver.find_element(locator_type, locator_value)
        await element.send_keys(text)
        await element.clear()
