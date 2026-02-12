import time

from pytest import raises

from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP
from caqui.exceptions import WebDriverError


class TestSyncCDPDriver:
    def test_cdp_refresh_page(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground

        element_before = driver.find_element(By.XPATH, "//input")
        driver.refresh()

        element_after = driver.find_element(By.XPATH, "//input")
        assert element_before != element_after

        element_before = element_after
        driver.refresh()

        element_after = driver.find_element(By.XPATH, "//input")
        assert element_before != element_after

        element_after = driver.find_element(By.XPATH, "//input")
        assert element_before != element_after

    def test_cdp_implicity_wait_is_deprecated(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        assert driver.implicitly_wait(3) is None

    def test_cdp_go_forward(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        title = "Sample page"
        driver.back()
        driver.forward()
        time.sleep(0.1)
        assert driver.get_title() == title

    def test_cdp_set_window_rectangle(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        window_rectangle_before = driver.get_window_size()
        x = window_rectangle_before.get("width", 0) + 1
        y = window_rectangle_before.get("height", 0) + 1

        driver.set_window_size(width=x, height=y)
        window_rectangle_after = driver.get_window_size()

        assert window_rectangle_after != window_rectangle_before
        assert window_rectangle_after.get("height") != window_rectangle_before.get("height")
        assert window_rectangle_after.get("width") != window_rectangle_before.get("width")

    def test_cdp_fullscreen_window(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        window_rectangle_before = driver.get_window_size()
        driver.fullscreen_window()
        window_rectangle_after = driver.get_window_size()
        assert window_rectangle_after != window_rectangle_before

    def test_cdp_minimize_window(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver.minimize_window()

    def test_cdp_maximize_window_asynchronous(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver.maximize_window()

    def test_cdp_new_window(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        assert driver.switch_to.new_window() is not None

    def test_cdp_take_screenshot_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        element = driver.find_element(locator_type, locator_value)
        element.screenshot("/tmp/picture.png")

    def test_cdp_take_screenshot(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver.save_screenshot("/tmp/picture.png")

    def test_cdp_get_computed_label(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        expected = "alert"

        element = driver.find_element(locator_type, locator_value)

        assert element.get_computed_label() == expected

    def test_cdp_get_computed_role(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        expected = "textbox"

        element = driver.find_element(locator_type, locator_value)

        assert element.get_computed_role() == expected

    def test_cdp_get_tag_name(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        expected = "INPUT"

        element = driver.find_element(locator_type, locator_value)

        assert element.get_tag_name() == expected

    def test_cdp_get_rect(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"

        element = driver.find_element(locator_type, locator_value)

        actual = element.get_rect()
        assert actual["height"]
        assert actual["width"]
        assert actual["x"]
        assert actual["y"]

    def test_cdp_move_to_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = driver.find_element(locator_type, locator_value)
        driver.actions.move_to_element(element).perform()

    def test_cdp_actions_scroll_to_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = driver.find_element(locator_type, locator_value)
        driver.actions.scroll_to_element(element).perform()

    def test_cdp_submit_foo(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.NAME
        locator_value = "my-form"

        element = driver.find_element(locator_type, locator_value)
        element.submit()

    def test_cdp_actions_click(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"

        element = driver.find_element(locator_type, locator_value)
        driver.actions.click(element).perform()

    def test_cdp_raise_exception_when_element_not_found(
        self, setup_sync_cdp_playground: SyncDriverCDP
    ):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//invalid-tag"

        with raises(WebDriverError):
            driver.find_element(locator_type, locator_value)

    def test_cdp_find_children_elements(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = 1  # parent inclusive
        locator_type = By.XPATH
        locator_value = "//div"

        parent_element = driver.find_element(locator_type, '//div[@class="parent"]')

        children_elements = parent_element.find_elements(locator_type, locator_value)

        assert len(children_elements) > expected

    def test_cdp_find_child_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "any4"
        locator_type = By.XPATH
        locator_value = '//div[@class="child4"]'

        parent_element = driver.find_element(locator_type, '//div[@class="parent"]')
        child_element = parent_element.find_element(locator_type, locator_value)
        text = child_element.get_text()
        assert text == expected

    def test_cdp_get_page_source(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "Sample page"

        assert expected in driver.get_page_source()

    def test_cdp_execute_script_asynchronous(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        script = "alert('any warn')"
        script = "style.background='#000000'"

        assert driver.execute_script(script) is None

    def test_cdp_get_alert_text(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.CSS_SELECTOR
        locator_value = "#alert-button"
        expected = "any warn"
        driver.find_element(locator_type, locator_value)
        assert driver.alert.get_text() == expected

    def test_cdp_get_active_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        locator_value = '//*[@id="button"]'

        element = driver.find_element(locator_type, locator_value)
        element.send_keys("any")

        element = driver.switch_to.get_active_element()
        assert element.get_text() == element.get_text()

    def test_cdp_clear_element_foo(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        text = "any"

        element = driver.find_element(locator_type, locator_value)
        element.send_keys(text)
        element.clear()
