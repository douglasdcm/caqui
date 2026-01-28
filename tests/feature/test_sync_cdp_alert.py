from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP


class TestSyncCDPAlert:
    def test_sync_cdp_send_alert_text(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button-prompt"
        driver.find_element(locator_type, locator_value)
        driver.alert.send_keys(text="any1")

    def test_sync_cdp_accept_alert(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        driver.find_element(locator_type, locator_value)
        driver.alert.accept()

    def test_sync_cdp_dismiss_alert(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        driver.find_element(locator_type, locator_value)
        driver.alert.dismiss()
