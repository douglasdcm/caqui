from caqui.cdp.by import By
from caqui.easy.cdp.synchronous.drivers import SyncDriverCDP


class TestSyncCDPObject:
    def test_cdp_action_chains(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(By.XPATH, "//button")
        (
            driver.actions.move_to_element(element)
            .scroll_to_element(element)
            .click(element)
            .perform()
        )

    def test_cdp_save_screenshot(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        assert driver.save_screenshot("/tmp/test.png") is None

    def test_cdp_object_to_string(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == f"type: Element. NodeId: {element.element_id}"

    def test_cdp_get_computed_role(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//button")
        assert element.get_computed_role() == "button"

    def test_cdp_get_computed_label(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//button")
        assert element.get_computed_label() == "test"

    def test_cdp_get_attribute_foo(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//input")
        assert element.get_attribute(attribute="value") == ""

    def test_cdp_clear(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//input")
        element.clear()

    #
    # def test_cdp_text_property(self, setup_sync_cdp_playground: AsyncDriver):
    #     driver = setup_sync_cdp_playground
    #     element = driver.find_element(locator=By.XPATH, value="//button")
    #     assert element.text == "test"

    def test_cdp_send_keys(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.ID, value="input")
        element.send_keys(text="any")
        assert element.get_text() == "any"

    def test_cdp_click(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//body")
        element.click()

    def test_cdp_find_elements_from_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = 1
        element = driver.find_element(locator=By.XPATH, value="//body")
        actual = element.find_elements(By.XPATH, "//button")
        assert len(actual) >= expected

    def test_cdp_find_element_from_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        element = driver.find_element(locator=By.XPATH, value="//body")
        actual = element.find_element(By.XPATH, "//button")
        assert actual is not None

    def test_cdp_find_elements(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = 1
        actual = driver.find_elements(locator=By.XPATH, value="//button")
        assert len(actual) >= expected

    def test_cdp_find_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        assert driver.find_element(locator=By.XPATH, value="//button") is not None
