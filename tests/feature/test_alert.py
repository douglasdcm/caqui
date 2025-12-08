import aiohttp
from pytest import mark, raises

from caqui import synchronous
from caqui.by import By
from caqui.easy.drivers import AsyncDriver
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, OTHER_URL, PAGE_URL

@mark.asyncio
async def test_send_alert_text(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button-prompt"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()
    assert await driver.alert.send_keys(text="any1") is True
    await driver.alert.accept() is True

    await element.click()
    assert await driver.alert.send_keys("any2") is True
    await driver.alert.accept() is True

    await element.click()


@mark.asyncio
async def test_accept_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()

    assert await driver.alert.accept() is True


@mark.asyncio
async def test_dismiss_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()
    assert await driver.alert.dismiss() is True

