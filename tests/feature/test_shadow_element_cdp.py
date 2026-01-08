from pytest import mark

from caqui.cdp.by import By
from caqui.easy.cdp.drivers import AsyncDriver


class TestCDPShadowElement:
    @mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
    @mark.asyncio
    async def test_cdp_find_elements_from_shadow_root(
        self, setup_cdp_playground: AsyncDriver, locator, value
    ):
        driver = setup_cdp_playground
        locator_type = By.ID
        locator_value = "shadow-root"
        expected = "Click Shadow"

        shadow_host = await driver.find_element(locator_type, locator_value)
        shadow_root = shadow_host.shadow_root
        shadow_content = await shadow_root.find_elements(locator, value)
        actual = await shadow_content[0].get_text()

        assert actual == expected

    @mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
    @mark.asyncio
    async def test_cdp_find_element_from_shadow_root(
        self, setup_cdp_playground: AsyncDriver, locator, value
    ):
        driver = setup_cdp_playground
        locator_type = By.ID
        locator_value = "shadow-root"
        expected = "Click Shadow"

        shadow_host = await driver.find_element(locator_type, locator_value)
        shadow_root = shadow_host.shadow_root
        shadow_content = await shadow_root.find_element(locator, value)
        actual = await shadow_content.get_text()

        assert actual == expected
