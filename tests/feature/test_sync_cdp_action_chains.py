from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP


class TestSyncCDPActionsChains:
    def test_sync_cdp_click(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(By.ID, "button")
        driver.actions.click(element).perform()
        assert element.get_css_value("color") == "red"

    def test_sync_cdp_move_to_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        h2 = driver.find_element(By.XPATH, "//h2[text()='Tooltips and Popovers']")
        assert h2.get_text() == "Tooltips and Popovers"
        tooltip = driver.find_element(By.XPATH, "//div[@class='tooltip']")
        driver.actions.scroll_to_element(h2).move_to_element(tooltip).perform()
        assert "This is a toolti" in tooltip.get_text()

    def test_sync_cdp_click_without_move_to_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(By.CSS_SELECTOR, "#app>button")
        driver.actions.click(element).perform()

    def test_sync_cdp_scroll_to_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(By.CSS_SELECTOR, "#app>button")
        driver.actions.scroll_to_element(element).perform()
        element.click()

    def test_sync_cdp_click_without_scroll_to_element(
        self, setup_sync_cdp_playground: SyncDriverCDP
    ):
        driver = setup_sync_cdp_playground
        element = driver.find_element(By.CSS_SELECTOR, "#app>button")
        element.click()
