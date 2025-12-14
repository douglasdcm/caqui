import time
from pytest import mark

from caqui.by import By
from caqui.easy.cdp.drivers import AsyncDriver


class TestCDPSwitchTo:
    @mark.asyncio
    async def test_cdp_switch_to_window_foo(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        await driver.switch_to.new_window()
        handles = await driver.get_window_handles()
        sample_page = handles[0]
        new_page = handles[1]
        assert await driver.switch_to.window(window_handle=new_page) is None
        # Retry the operation if the page  is not ready
        for _ in range(10):
            try:
                assert await driver.get_title() == "about:blank"
                break
            except AssertionError:
                time.sleep(0.1)
        await driver.get("http://example.com")
        assert await driver.get_title() == "Example Domain"
        await driver.switch_to.window(window_handle=sample_page) is None
        assert await driver.get_title() == "Sample page"

    @mark.asyncio
    async def test_cdp_switch_to_parent_frame_asynchronous(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.ID
        locator_value = "my-iframe"

        element_frame = await driver.find_element(locator_type, locator_value)
        await driver.switch_to.frame(element_frame)

    @mark.asyncio
    async def test_cdp_switch_to_frame_asynchronous(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.ID
        locator_value = "my-iframe"
        locator_type_form = "css selector"
        locator_form = "body > form"

        element_form = await driver.find_element(locator_type_form, locator_form)
        await driver.actions.scroll_to_element(element_form, delta_y=1000).perform()

        element_frame = await driver.find_element(locator_type, locator_value)
        await driver.switch_to.frame(element_frame)
