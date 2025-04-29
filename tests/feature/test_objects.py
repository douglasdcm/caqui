from caqui.easy import AsyncPage, ActionChains
from caqui.by import By
from pytest import mark
from caqui import synchronous


class TestObject:
    @mark.asyncio
    async def test_action_chains(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(By.XPATH, "//button")
        actions = (
            await driver.actions.move_to_element(element)
            .scroll_to_element(element)
            .click(element)
            .perform()
        )
        assert actions is True

        actions = (
            await ActionChains(driver)
            .move_to_element(element)
            .scroll_to_element(element)
            .click(element)
            .perform()
        )
        assert actions is True

    @mark.asyncio
    async def test_save_screenshot(self, setup_environment: AsyncPage):
        driver = setup_environment

        assert await driver.save_screenshot("/tmp/test.png") is True

    @mark.asyncio
    async def test_object_to_string(self, setup_environment: AsyncPage):
        driver = setup_environment

        element_string = synchronous.find_element(
            driver.remote, driver.session, By.XPATH, "//button"
        )
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == element_string

    @mark.asyncio
    async def test_get_computed_role(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_role() == "button"

    @mark.asyncio
    async def test_get_computed_label(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_label() == "test"

    @mark.asyncio
    async def test_get_attribute(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//input")
        assert await element.get_attribute(attribute="value") == ""

    @mark.asyncio
    async def test_clear(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//input")
        assert await element.clear() is True

    @mark.asyncio
    async def test_text_property(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert element.text == "test"

    @mark.asyncio
    async def test_send_keys(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//body")
        assert await element.send_keys(text="any") is True

    @mark.asyncio
    async def test_click(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//body")
        assert await element.click() is True

    @mark.asyncio
    async def test_find_elements_from_element(self, setup_environment: AsyncPage):
        driver = setup_environment
        expected = 1
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_elements(By.XPATH, "//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element_from_element(self, setup_environment: AsyncPage):
        driver = setup_environment
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_element(By.XPATH, "//button")
        assert actual is not None

    @mark.asyncio
    async def test_find_elements(self, setup_environment: AsyncPage):
        driver = setup_environment
        expected = 1
        actual = await driver.find_elements(locator=By.XPATH, value="//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element(self, setup_environment: AsyncPage):
        driver = setup_environment
        assert await driver.find_element(locator=By.XPATH, value="//button") is not None
