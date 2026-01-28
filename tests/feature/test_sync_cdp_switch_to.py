import time

from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP


class TestSyncCDPSwitchTo:
    def test_cdp_switch_to_window_foo(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver.switch_to.new_window()
        handles = driver.get_window_handles()
        sample_page = handles[0]
        new_page = handles[1]
        assert driver.switch_to.window(window_handle=new_page) is None
        # Retry the operation if the page is not ready
        for _ in range(10):
            try:
                assert driver.get_title() == "about:blank"
                break
            except AssertionError:
                time.sleep(0.1)
        driver.get("http://example.com")
        assert driver.get_title() == "Example Domain"
        driver.switch_to.window(window_handle=sample_page) is None
        assert driver.get_title() == "Sample page"

    def test_cdp_switch_to_parent_frame_asynchronous(
        self, setup_sync_cdp_playground: SyncDriverCDP
    ):
        driver = setup_sync_cdp_playground
        locator_type = By.ID
        locator_value = "my-iframe"

        element_frame = driver.find_element(locator_type, locator_value)
        driver.switch_to.frame(element_frame)

    def test_cdp_switch_to_frame_asynchronous(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.ID
        locator_value = "my-iframe"
        locator_type_form = "css selector"
        locator_form = "body > form"

        element_form = driver.find_element(locator_type_form, locator_form)
        driver.actions.scroll_to_element(element_form, delta_y=1000).perform()

        element_frame = driver.find_element(locator_type, locator_value)
        driver.switch_to.frame(element_frame)
