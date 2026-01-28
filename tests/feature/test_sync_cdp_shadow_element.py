from pytest import mark

from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP


class TestSyncCDPShadowElement:
    @mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
    def test_cdp_find_elements_from_shadow_root(
        self, setup_sync_cdp_playground: SyncDriverCDP, locator, value
    ):
        driver = setup_sync_cdp_playground
        locator_type = By.ID
        locator_value = "shadow-root"
        expected = "Click Shadow"

        shadow_host = driver.find_element(locator_type, locator_value)
        shadow_root = shadow_host.shadow_root
        shadow_content = shadow_root.find_elements(locator, value)
        actual = shadow_content[0].get_text()

        assert actual == expected

    @mark.parametrize("locator, value", [(By.ID, "shadow-button"), (By.CSS_SELECTOR, "button")])
    def test_cdp_find_element_from_shadow_root(
        self, setup_sync_cdp_playground: SyncDriverCDP, locator, value
    ):
        driver = setup_sync_cdp_playground
        locator_type = By.ID
        locator_value = "shadow-root"
        expected = "Click Shadow"

        shadow_host = driver.find_element(locator_type, locator_value)
        shadow_root = shadow_host.shadow_root
        shadow_content = shadow_root.find_element(locator, value)
        actual = shadow_content.get_text()

        assert actual == expected
