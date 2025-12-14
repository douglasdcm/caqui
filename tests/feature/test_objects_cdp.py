from pytest import mark

from caqui.by import By
from caqui.easy.cdp.drivers import AsyncDriver


class TestCDPObject:
    @mark.asyncio
    async def test_cdp_action_chains(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(By.XPATH, "//button")
        (
            await driver.actions.move_to_element(element)
            .scroll_to_element(element)
            .click(element)
            .perform()
        )

    @mark.asyncio
    async def test_cdp_save_screenshot(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        assert await driver.save_screenshot("/tmp/test.png") is None

    @mark.asyncio
    async def test_cdp_object_to_string(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == f"type: Element. NodeId: {element.element_id}"

    @mark.asyncio
    async def test_cdp_get_computed_role(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_role() == "button"

    @mark.asyncio
    async def test_cdp_get_computed_label(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_label() == "test"

    @mark.asyncio
    async def test_cdp_get_attribute_foo(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//input")
        assert await element.get_attribute(attribute="value") == ""

    @mark.asyncio
    async def test_cdp_clear(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//input")
        await element.clear()

    # @mark.asyncio
    # async def test_cdp_text_property(self, setup_cdp_playground: AsyncDriver):
    #     driver = setup_cdp_playground
    #     element = await driver.find_element(locator=By.XPATH, value="//button")
    #     assert element.text == "test"

    @mark.asyncio
    async def test_cdp_send_keys(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.ID, value="input")
        await element.send_keys(text="any")
        assert await element.get_text() == "any"

    @mark.asyncio
    async def test_cdp_click(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//body")
        await element.click()

    @mark.asyncio
    async def test_cdp_find_elements_from_element(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = 1
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_elements(By.XPATH, "//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_cdp_find_element_from_element(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_element(By.XPATH, "//button")
        assert actual is not None

    @mark.asyncio
    async def test_cdp_find_elements(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = 1
        actual = await driver.find_elements(locator=By.XPATH, value="//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_cdp_find_element(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        assert await driver.find_element(locator=By.XPATH, value="//button") is not None
