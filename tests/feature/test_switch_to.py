import aiohttp
from pytest import mark, raises

from caqui import synchronous
from caqui.by import By
from caqui.easy.action_chains import ActionChains
from caqui.easy.drivers import AsyncDriver
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, OTHER_URL, PAGE_URL

@mark.parametrize("window_type", ("tab", "window"))
@mark.asyncio
async def test_switch_to_window_foo(setup_playground: AsyncDriver, window_type):
    driver = setup_playground

    await driver.switch_to.new_window(window_type)
    handles = driver.window_handles
    sample_page = handles[0]
    new_page = handles[1]

    assert await driver.switch_to.window(window_handle=new_page) is True
    assert driver.title == ""
    await driver.switch_to.window(window_handle=sample_page) is True

    assert await driver.switch_to.window(window_handle=new_page) is True
    assert driver.title == ""

@mark.asyncio
async def test_switch_to_parent_frame_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True




@mark.asyncio
async def test_switch_to_frame_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.ID
    locator_value = "my-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.scroll_to_element(element_form, delta_y=1000).perform()

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True


