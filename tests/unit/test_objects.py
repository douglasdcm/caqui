from caqui.caqui import AsyncDriver
from caqui import by
from pytest import mark, fixture
from tests.constants import PAGE_URL


class TestObject:
    @fixture
    def setup(self):
        remote = "http://127.0.0.1:9999"
        capabilities = {
            "desiredCapabilities": {
                by.NAME: "webdriver",
                "browserName": "chrome",
                "marionette": False,
                "acceptInsecureCerts": True,
                "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
            }
        }
        driver = AsyncDriver(remote, capabilities, PAGE_URL)
        yield driver
        driver.quit()

    @mark.asyncio
    async def test_get_computed_label(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//button")
        assert await element.get_computed_label() == "test"

    @mark.asyncio
    async def test_get_attribute(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//input")
        assert await element.get_attribute(attribute="value") == ""

    @mark.asyncio
    async def test_clear(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//input")
        assert await element.clear() is True

    @mark.asyncio
    async def test_send_keys(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//body")
        assert await element.send_keys(text="any") is True

    @mark.asyncio
    async def test_click(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//body")
        assert await element.click() is True

    @mark.asyncio
    async def test_find_elements_from_element(self, setup: AsyncDriver):
        driver = setup
        expected = 1
        element = await driver.find_element(locator=by.XPATH, value="//body")
        actual = await element.find_elements(by.XPATH, "//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element_from_element(self, setup: AsyncDriver):
        driver = setup
        element = await driver.find_element(locator=by.XPATH, value="//body")
        assert await element.find_element(by.XPATH, "//button") is not None

    @mark.asyncio
    async def test_find_elements(self, setup: AsyncDriver):
        driver = setup
        expected = 1
        actual = await driver.find_elements(locator=by.XPATH, value="//button")
        assert len(actual) >= expected

    @mark.asyncio
    async def test_find_element(self, setup: AsyncDriver):
        driver = setup
        assert await driver.find_element(locator=by.XPATH, value="//button") is not None
