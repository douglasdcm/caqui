from pytest import mark

from caqui.cdp.by import By
from caqui.easy.cdp.asynchronous.drivers import AsyncDriverCDP


class TestCDPAlert:
    @mark.asyncio
    async def test_cdp_send_alert_text(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button-prompt"
        await driver.find_element(locator_type, locator_value)
        await driver.alert.send_keys(text="any1")

    @mark.asyncio
    async def test_cdp_accept_alert(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        await driver.find_element(locator_type, locator_value)
        await driver.alert.accept()

    @mark.asyncio
    async def test_cdp_dismiss_alert(self, setup_cdp_playground: AsyncDriverCDP):
        driver = setup_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        await driver.find_element(locator_type, locator_value)
        await driver.alert.dismiss()
