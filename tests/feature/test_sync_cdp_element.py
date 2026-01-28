import time

from pytest import raises

from caqui.cdp.by import By
from caqui.cdp.synchronous.drivers import SyncDriverCDP
from caqui.exceptions import WebDriverError
from tests.constants import OTHER_URL


class TestSyncCDPElement:
    def test_cdp_is_element_enabled(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        element = driver.find_element(locator_type, locator_value)
        assert element.is_enabled() is True

    def elementt_css_value(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        property_name = "color"
        expected = "0, 0, 0"
        element = driver.find_element(locator_type, locator_value)
        assert expected in element.get_css_value(property_name)

    def test_cdp_is_element_selected(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        element = driver.find_element(locator_type, locator_value)
        assert element.is_selected() is False

    def test_cdp_get_window_rectangle(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "height"
        rectangle = driver.get_window_size()
        assert expected in rectangle

    def test_cdp_get_window_handles(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        handles = driver.get_window_handles()
        assert isinstance(handles, list)

    def test_cdp_get_window(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        assert driver.window is not None

    def test_cdp_get_attribute_raise_exception_when_invalid_attribute(
        self, setup_sync_cdp_playground: SyncDriverCDP
    ):
        driver = setup_sync_cdp_playground
        attribute = "invalid"
        element = driver.find_element(By.XPATH, "//a[@id='a1']")
        with raises(WebDriverError):
            element.get_attribute(attribute)

    def test_cdp_get_attribute(self, setup_sync_cdp_playground: SyncDriverCDP):
        expected = "http://any1.com"
        driver = setup_sync_cdp_playground
        attribute = "href"
        element = driver.find_element(By.XPATH, "//a[@id='a1']")
        assert expected in element.get_attribute(attribute)

    def test_cdp_get_cookies(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        cookies = driver.get_cookies()
        assert isinstance(cookies, list)

    def test_cdp_go_back(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        title_sample = "Sample page"
        title_other = "Other page"

        driver.get(OTHER_URL)
        driver.back()
        time.sleep(0.1)
        assert driver.get_title() == title_sample
        driver.forward()
        time.sleep(0.1)
        assert driver.get_title() == title_other

    def test_cdp_get_url(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "playground.html"
        actual = driver.get_current_url()
        assert expected in actual

    def test_cdp_get_title(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "Sample page"
        assert driver.get_title() == expected

    def test_cdp_find_elements_fails_when_invalid_data_input(
        self,
        setup_sync_cdp_playground: SyncDriverCDP,
    ):
        driver = setup_sync_cdp_playground
        locator_type = "invalid"
        locator_value = "//input"
        with raises(WebDriverError):
            driver.find_elements(locator_type, locator_value)

    def test_cdp_find_elements(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        elements = driver.find_elements(locator_type, locator_value)
        assert len(elements) > 0

    def test_cdp_find_element_fails_when_invalid_data_input(
        self, setup_sync_cdp_playground: SyncDriverCDP
    ):
        driver = setup_sync_cdp_playground
        locator_type = "invalid"
        locator_value = "//input"
        with raises(WebDriverError):
            driver.find_element(locator_type, locator_value)

    def test_cdp_find_element(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//input"
        assert driver.find_element(locator_type, locator_value) is not None

    def test_cdp_get_property(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        text = "any_value"
        locator_type = By.XPATH
        locator_value = "//input"
        property = "value"
        element = driver.find_element(locator_type, locator_value)
        element.send_keys(text)
        assert element.get_property(property) == ""

    def test_cdp_get_text(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        expected = "end"
        locator_type = By.XPATH
        locator_value = "//p[@id='end']"  # <p>end</p>
        element = driver.find_element(locator_type, locator_value)
        assert element.get_text() == expected

    def test_cdp_send_keys(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        text_ = "any_sync"
        locator_type = By.XPATH
        locator_value = "//input"
        element = driver.find_element(locator_type, locator_value)
        element.send_keys(text_)

    def test_cdp_click(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        locator_type = By.XPATH
        locator_value = "//button"
        element = driver.find_element(locator_type, locator_value)
        element.click()
