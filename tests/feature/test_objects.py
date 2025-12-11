from pytest import mark

from caqui import synchronous
from caqui.by import By
from caqui.easy import AsyncDriver


class TestObject:
    @mark.asyncio
    async def test_action_chains(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(By.XPATH, "//button")
        (
            await driver.actions.move_to_element(element)
            .scroll_to_element(element)
            .click(element)
            .perform()
        )

    @mark.asyncio
    async def test_save_screenshot(self, setup_playground: AsyncDriver):
        driver = setup_playground

        assert await driver.save_screenshot("/tmp/test.png") is True

    @mark.asyncio
    async def test_object_to_string(self, setup_playground: AsyncDriver):
        driver = setup_playground

        element_string = synchronous.find_element(
            driver.server_url, driver.session, By.XPATH, "//button"
        )
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == element_string

    @mark.asyncio
    async def test_get_computed_role(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_role() == "button"

    @mark.asyncio
    async def test_get_computed_label(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert await element.get_computed_label() == "test"

    @mark.asyncio
    async def test_get_attribute(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//input")
        assert await element.get_attribute(attribute="value") == ""

    @mark.asyncio
    async def test_clear(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//input")
        await element.clear()

    @mark.asyncio
    async def test_text_property(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert element.text == "test"

    @mark.asyncio
    async def test_send_keys(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//body")
        await element.send_keys(text="any")
        assert element.text == "any"

    @mark.asyncio
    async def test_click(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//body")
        await element.click()

    @mark.asyncio
    async def test_find_elements_from_element(self, setup_playground: AsyncDriver):
        driver = setup_playground
        expected = 1
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_elements(By.XPATH, "//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element_from_element(self, setup_playground: AsyncDriver):
        driver = setup_playground
        element = await driver.find_element(locator=By.XPATH, value="//body")
        actual = await element.find_element(By.XPATH, "//button")
        assert actual is not None

    @mark.asyncio
    async def test_find_elements(self, setup_playground: AsyncDriver):
        driver = setup_playground
        expected = 1
        actual = await driver.find_elements(locator=By.XPATH, value="//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element(self, setup_playground: AsyncDriver):
        driver = setup_playground
        assert await driver.find_element(locator=By.XPATH, value="//button") is not None
