import aiohttp
from pytest import mark, raises

from caqui import synchronous
from caqui.by import By
from caqui.easy.drivers import AsyncDriver
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, OTHER_URL, PAGE_URL


@mark.asyncio
async def test_is_element_enabled(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    element = await driver.find_element(locator_type, locator_value)

    assert await element.is_enabled() is True


@mark.asyncio
async def elementt_css_value(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"
    property_name = "color"
    expected = "0, 0, 0"

    element = await driver.find_element(locator_type, locator_value)

    assert expected in await element.get_css_value(property_name)


@mark.asyncio
async def test_is_element_selected(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    element = await driver.find_element(locator_type, locator_value)

    assert await element.is_selected() is False


@mark.asyncio
async def test_get_window_rectangle(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "height"

    rectangle = await driver.get_window_size()
    assert expected in rectangle


@mark.asyncio
async def test_get_window_handles(setup_playground: AsyncDriver):
    driver = setup_playground

    handles = driver.window_handles
    assert isinstance(handles, list)


@mark.asyncio
async def test_close_window_async(setup_playground: AsyncDriver):
    driver = setup_playground

    response = await driver.close()
    assert isinstance(response, list)


@mark.asyncio
async def test_get_window(setup_playground: AsyncDriver):
    driver = setup_playground

    assert driver.window is not None


@mark.asyncio
async def test_get_attribute_send_empty_value_when_invalid_attribute(setup_playground: AsyncDriver):
    driver = setup_playground
    attribute = "invalid"
    element = await driver.find_element(By.XPATH, "//a[@id='a1']")

    assert "" == await element.get_attribute(attribute)


@mark.asyncio
async def test_get_attribute(setup_playground: AsyncDriver):
    expected = "http://any1.com"
    driver = setup_playground
    attribute = "href"
    element = await driver.find_element(By.XPATH, "//a[@id='a1']")

    assert expected in await element.get_attribute(attribute)


@mark.asyncio
async def test_get_cookies(setup_playground: AsyncDriver):
    driver = setup_playground
    cookies = await driver.get_cookies()
    assert isinstance(cookies, list)


@mark.asyncio
async def test_go_back(setup_playground: AsyncDriver):
    driver = setup_playground
    title_sample = "Sample page"
    title_other = "Other page"

    await driver.get(OTHER_URL)
    assert await driver.back() is True
    assert driver.title == title_sample

    await driver.forward() is True
    assert driver.title == title_other


@mark.asyncio
async def test_get_url(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "playground.html"

    assert expected in driver.current_url


@mark.asyncio
async def test_get_title(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "Sample page"

    assert driver.title == expected


@mark.asyncio
async def test_find_elements_fails_when_invalid_data_input(
    setup_playground: AsyncDriver,
):
    driver = setup_playground
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        await driver.find_elements(locator_type, locator_value)


@mark.asyncio
async def test_find_elements(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    elements = await driver.find_elements(locator_type, locator_value)

    assert len(elements) > 0


@mark.asyncio
async def test_find_element_fails_when_invalid_data_input(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = "invalid"
    locator_value = "//input"

    with raises(WebDriverError):
        await driver.find_element(locator_type, locator_value)


@mark.asyncio
async def test_find_element(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//input"

    assert await driver.find_element(locator_type, locator_value) is not None


@mark.asyncio
async def test_get_property(setup_playground: AsyncDriver):
    driver = setup_playground
    text = "any_value"
    locator_type = By.XPATH
    locator_value = "//input"
    property = "value"

    element = await driver.find_element(locator_type, locator_value)
    await element.send_keys(text)

    assert await element.get_property(property) == text


@mark.asyncio
async def test_get_text(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "end"
    locator_type = By.XPATH
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = await driver.find_element(locator_type, locator_value)

    assert await element.get_text() == expected


@mark.asyncio
async def test_send_keys(setup_playground: AsyncDriver):
    driver = setup_playground
    text_async = "any_async"
    locator_type = By.XPATH
    locator_value = "//input"

    element = await driver.find_element(locator_type, locator_value)

    assert await element.send_keys(text_async) is True


@mark.asyncio
async def test_click(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.XPATH
    locator_value = "//button"

    element = await driver.find_element(locator_type, locator_value)

    assert await element.click() is True
