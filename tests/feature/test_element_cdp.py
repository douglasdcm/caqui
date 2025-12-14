import time
from pytest import mark, raises
from caqui.by import By
from caqui.easy.cdp.drivers import AsyncDriver
from caqui.exceptions import WebDriverError
from tests.constants import OTHER_URL


class TestCDPElement:
    @mark.asyncio
    async def test_cdp_is_element_enabled(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        element = await driver.find_element(locator_type, locator_value)
        assert await element.is_enabled() is True

    @mark.asyncio
    async def elementt_css_value(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        property_name = "color"
        expected = "0, 0, 0"
        element = await driver.find_element(locator_type, locator_value)
        assert expected in await element.get_css_value(property_name)

    @mark.asyncio
    async def test_cdp_is_element_selected(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        element = await driver.find_element(locator_type, locator_value)
        assert await element.is_selected() is False

    @mark.asyncio
    async def test_cdp_get_window_rectangle(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = "height"
        rectangle = await driver.get_window_size()
        assert expected in rectangle

    @mark.asyncio
    async def test_cdp_get_window_handles(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        handles = await driver.get_window_handles()
        assert isinstance(handles, list)

    @mark.asyncio
    async def test_cdp_get_window(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        assert driver.window is not None

    @mark.asyncio
    async def test_cdp_get_attribute_raise_exception_when_invalid_attribute(
        self, setup_cdp_playground: AsyncDriver
    ):
        driver = setup_cdp_playground
        attribute = "invalid"
        element = await driver.find_element(By.XPATH, "//a[@id='a1']")
        with raises(WebDriverError):
            await element.get_attribute(attribute)

    @mark.asyncio
    async def test_cdp_get_attribute(self, setup_cdp_playground: AsyncDriver):
        expected = "http://any1.com"
        driver = setup_cdp_playground
        attribute = "href"
        element = await driver.find_element(By.XPATH, "//a[@id='a1']")
        assert expected in await element.get_attribute(attribute)

    @mark.asyncio
    async def test_cdp_get_cookies(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        cookies = await driver.get_cookies()
        assert isinstance(cookies, list)

    @mark.asyncio
    async def test_cdp_go_back(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        title_sample = "Sample page"
        title_other = "Other page"

        await driver.get(OTHER_URL)
        await driver.back()
        time.sleep(0.1)
        assert await driver.get_title() == title_sample
        await driver.forward()
        time.sleep(0.1)
        assert await driver.get_title() == title_other

    @mark.asyncio
    async def test_cdp_get_url(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = "playground.html"
        actual = await driver.get_current_url()
        assert expected in actual

    @mark.asyncio
    async def test_cdp_get_title(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = "Sample page"
        assert await driver.get_title() == expected

    @mark.asyncio
    async def test_cdp_find_elements_fails_when_invalid_data_input(
        self,
        setup_cdp_playground: AsyncDriver,
    ):
        driver = setup_cdp_playground
        locator_type = "invalid"
        locator_value = "//input"
        with raises(WebDriverError):
            await driver.find_elements(locator_type, locator_value)

    @mark.asyncio
    async def test_cdp_find_elements(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        elements = await driver.find_elements(locator_type, locator_value)
        assert len(elements) > 0

    @mark.asyncio
    async def test_cdp_find_element_fails_when_invalid_data_input(
        self, setup_cdp_playground: AsyncDriver
    ):
        driver = setup_cdp_playground
        locator_type = "invalid"
        locator_value = "//input"
        with raises(WebDriverError):
            await driver.find_element(locator_type, locator_value)

    @mark.asyncio
    async def test_cdp_find_element(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        assert await driver.find_element(locator_type, locator_value) is not None

    @mark.asyncio
    async def test_cdp_get_property(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        text = "any_value"
        locator_type = By.XPATH
        locator_value = "//input"
        property = "value"
        element = await driver.find_element(locator_type, locator_value)
        await element.send_keys(text)
        assert await element.get_property(property) == ""

    @mark.asyncio
    async def test_cdp_get_text(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        expected = "end"
        locator_type = By.XPATH
        locator_value = "//p[@id='end']"  # <p>end</p>
        element = await driver.find_element(locator_type, locator_value)
        assert await element.get_text() == expected

    @mark.asyncio
    async def test_cdp_send_keys(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        text_async = "any_async"
        locator_type = By.XPATH
        locator_value = "//input"
        element = await driver.find_element(locator_type, locator_value)
        await element.send_keys(text_async)

    @mark.asyncio
    async def test_cdp_click(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"
        element = await driver.find_element(locator_type, locator_value)
        await element.click()
