from pytest import mark

from caqui.cdp.by import By
from caqui.webdriver.drivers import AsyncDriver


@mark.asyncio
async def test_send_alert_text(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button-prompt"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()
    await driver.alert.send_keys(text="any1")
    await driver.alert.accept()

    await element.click()
    await driver.alert.send_keys("any2")
    await driver.alert.accept()

    await element.click()


@mark.asyncio
async def test_accept_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()
    await driver.alert.accept()


@mark.asyncio
async def test_dismiss_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = By.CSS_SELECTOR
    locator_value = "#alert-button"

    element = await driver.find_element(locator_type, locator_value)
    await element.click()
    await driver.alert.dismiss()
