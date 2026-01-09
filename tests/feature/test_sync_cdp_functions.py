from typing import Tuple

import pytest
from pytest import mark, raises

from caqui.cdp import synchronous
from caqui.cdp.by import By
from caqui.easy.cdp.server import LocalServerCDP, get_ws_url
from caqui.easy.cdp.synchronous.connection import SyncCDPConnection
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, PAGE_URL


class TestCDPSyncFunctionsBlankPage:
    PORT = 9223

    @pytest.fixture(autouse=True, scope="class")
    def launch_browser_(self):
        server = LocalServerCDP(self.PORT)
        server.start_edge()
        yield
        server.dispose()

    @pytest.fixture
    def setup_env(self):
        conn = SyncCDPConnection(get_ws_url(self.PORT))
        conn.connect()
        yield conn
        conn.close()

    def test_cdp_sync_get_title_from_blank_page(self, setup_env):
        handle = (synchronous.get_window_handles(setup_env))[0]
        new_conn = synchronous.switch_to_window(setup_env, handle)
        assert synchronous.get_title(new_conn) == "about:blank"

    def test_cdp_sync_get_body_from_blank_page(self, setup_env):
        handle = (synchronous.get_window_handles(setup_env))[0]
        new_conn = synchronous.switch_to_window(setup_env, handle)
        assert synchronous.find_element(new_conn, By.TAG_NAME, "body") is not None


class TestCDPSyncFunctions:
    @pytest.fixture
    def setup_env(self):
        conn = SyncCDPConnection(get_ws_url())
        conn.connect()
        synchronous.get(conn, PAGE_URL)
        synchronous.set_window_rectangle(conn, 1000, 1000, 0, 0)
        yield conn
        conn.close()

    def test_cdp_sync_find_element_by_xpath(self, setup_env):
        assert synchronous.find_element(setup_env, By.XPATH, "//*[@id='input']") is not None

    def test_cdp_sync_find_element_by_css_selector(self, setup_env):
        assert synchronous.find_element(setup_env, By.CSS_SELECTOR, "#input") is not None

    def test_cdp_sync_find_element_by_id(self, setup_env):
        assert synchronous.find_element(setup_env, By.ID, "input") is not None

    def test_cdp_sync_find_element_by_class_name(self, setup_env):
        assert synchronous.find_element(setup_env, By.CLASS_NAME, "my-class") is not None

    def test_cdp_sync_find_element_invalid(self, setup_env):
        with raises(WebDriverError):
            synchronous.find_element(setup_env, By.XPATH, "invalid")

    def test_cdp_sync_get_shadow_element(self, setup_env):
        shadow_element = synchronous.find_element(setup_env, By.ID, "shadow-root")
        element = synchronous.get_shadow_element(setup_env, shadow_element, By.ID, "shadow-button")
        assert synchronous.get_tag_name(setup_env, element) == "BUTTON"

    def test_cdp_sync_get_shadow_elements(self, setup_env):
        shadow_element = synchronous.find_element(setup_env, By.ID, "shadow-root")
        element = (
            synchronous.get_shadow_elements(setup_env, shadow_element, By.ID, "shadow-button")
        )[0]
        assert synchronous.get_tag_name(setup_env, element) == "BUTTON"

    @mark.parametrize(
        "locator",
        [
            (By.CSS_SELECTOR, "#input"),
            (By.ID, "input"),
            (By.TAG_NAME, "input"),
            (By.CLASS_NAME, "my-class"),
            (By.XPATH, "//input"),
            (By.NAME, "my-form"),
            (By.PARTIAL_LINK_TEXT, "parent"),
            (By.LINK_TEXT, "parent.com\n        "),
        ],
    )
    def test_cdp_sync_find_elements(self, setup_env, locator: Tuple):
        assert synchronous.find_elements(setup_env, *locator) is not None

    def test_cdp_sync_click_foo(self, setup_env):
        element = synchronous.find_element(setup_env, By.CSS_SELECTOR, "#button")
        assert synchronous.click(setup_env, element) is None

    def test_cdp_sync_send_keys(self, setup_env):
        element = synchronous.find_element(setup_env, By.XPATH, "//*[@id='input']")
        assert synchronous.send_keys(setup_env, element, text="caqui") is None

    def test_cdp_sync_get_text(self, setup_env):
        expected = "Basic page"
        element = synchronous.find_element(setup_env, By.XPATH, "//h1")
        assert synchronous.get_text(setup_env, element) == expected

    def test_cdp_sync_get_attribute_style(self, setup_env):
        expected = "color: red;"
        element = synchronous.find_element(setup_env, By.ID, "button")
        synchronous.click(setup_env, element)
        assert synchronous.get_attribute(setup_env, element, "style") == expected

    def test_cdp_sync_get_attribute_href(self, setup_env):
        expected = "http://any1.com"
        element = synchronous.find_element(setup_env, By.ID, "a1")
        assert synchronous.get_attribute(setup_env, element, "href") == expected

    def test_cdp_sync_get_title(self, setup_env):
        expected = "Sample page"
        assert synchronous.get_title(setup_env) == expected

    def test_cdp_sync_get_url(self, setup_env):
        expected = "file:///home/douglas/repo/caqui/tests/html/playground.html"
        assert synchronous.get_url(setup_env) == expected

    def test_cdp_sync_go_back(self, setup_env):
        assert synchronous.go_back(setup_env) is None

    def test_cdp_sync_element_is_selected(self, setup_env):
        element = synchronous.find_element(setup_env, By.CSS_SELECTOR, "#interest-tech")
        assert synchronous.is_element_selected(setup_env, element) is True

    def test_cdp_sync_element_is_not_selected(self, setup_env):
        element = synchronous.find_element(setup_env, By.CSS_SELECTOR, "#interest-sports")
        assert synchronous.is_element_selected(setup_env, element) is False

    def test_cdp_sync_get_css_value(self, setup_env):
        expected = "red"
        element = synchronous.find_element(setup_env, By.ID, "button")
        synchronous.click(setup_env, element)
        assert synchronous.get_css_value(setup_env, element, "color") == expected

    def test_cdp_sync_handle_cookie(self, setup_env):
        synchronous.get(setup_env, "https://example.org/")
        synchronous.add_cookie(setup_env, COOKIE)
        cookie = synchronous.get_named_cookie(setup_env, COOKIE.get("name"))
        assert cookie.get("name") == COOKIE.get("name")
        assert (
            synchronous.delete_cookie(
                setup_env, COOKIE.get("name"), COOKIE.get("url"), COOKIE.get("domain")
            )
            is None
        )

    def test_cdp_sync_get_cookies(self, setup_env):
        synchronous.get(setup_env, "https://example.org/")
        synchronous.add_cookie(setup_env, COOKIE)
        actual = synchronous.get_cookies(setup_env)
        assert len(actual) > 0

    def test_cdp_sync_delete_all_cookies(self, setup_env):
        synchronous.get(setup_env, "https://example.org/")
        synchronous.add_cookie(setup_env, COOKIE)
        assert (
            synchronous.delete_all_cookies(
                setup_env,
            )
            is None
        )

    def test_cdp_sync_refresh_page(self, setup_env):
        assert synchronous.refresh_page(setup_env) is None

    def test_cdp_sync_go_forward(self, setup_env):
        synchronous.get(setup_env, "https://example.org/")
        synchronous.go_back(setup_env)
        assert synchronous.go_forward(setup_env) is None

    def test_cdp_sync_set_window_rectangle(self, setup_env):
        assert synchronous.set_window_rectangle(setup_env, width=300, height=300) is None

    def test_cdp_sync_set_fullscreen(self, setup_env):
        assert synchronous.fullscreen_window(setup_env) is None

    def test_cdp_sync_minimized(self, setup_env):
        assert synchronous.minimize_window(setup_env) is None

    def test_cdp_sync_set_maximized(self, setup_env):
        assert synchronous.maximize_window(setup_env) is None

    def test_cdp_sync_get_window_handlers(self, setup_env):
        assert len(synchronous.get_window_handles(setup_env)) > 0

    def test_cdp_sync_new_window(self, setup_env):
        synchronous.new_window(setup_env) is None
        assert len(synchronous.get_window_handles(setup_env)) > 1

    def test_cdp_sync_switch_to_window_tmp(self, setup_env):
        synchronous.get(setup_env, PAGE_URL)
        synchronous.new_window(setup_env) is None
        handles = synchronous.get_window_handles(setup_env)
        synchronous.switch_to_window(setup_env, handles[-1]) is not None

    def test_cdp_sync_switch_to_frame(self, setup_env):
        iframe_id = synchronous.find_element(setup_env, By.ID, "my-iframe")
        iframe_node = synchronous.switch_to_frame(setup_env, iframe_id)
        assert iframe_node is not None

        element = synchronous.find_element(setup_env, By.ID, "alert-button-iframe", iframe_node)
        assert synchronous.get_attribute(setup_env, element, "any") == "any"

    def test_cdp_sync_switch_to_parent_frame(self, setup_env):
        iframe_id = synchronous.find_element(setup_env, By.ID, "my-iframe")
        iframe_node = synchronous.switch_to_frame(setup_env, iframe_id)
        synchronous.find_element(setup_env, By.ID, "alert-button-iframe", iframe_node)
        parent_frame = synchronous.switch_to_parent_frame(setup_env)
        assert parent_frame is not None
        with raises(WebDriverError):
            synchronous.find_element(setup_env, By.ID, "alert-button-iframe")

    def test_cdp_sync_send_alert_text_foo(self, setup_env):
        alert = synchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert synchronous.send_alert_text(setup_env, alert, "any") is None

    def test_cdp_sync_send_alert_text_fails_if_no_alert(self, setup_env):
        no_alert = synchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert synchronous.send_alert_text(setup_env, no_alert, "any", 0.1) is None

    def test_cdp_sync_accept_alert(self, setup_env):
        alert = synchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert synchronous.accept_alert(setup_env, alert) is None

    def test_cdp_sync_accept_alert_fails_if_no_alert(self, setup_env):
        no_alert = synchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert synchronous.accept_alert(setup_env, no_alert, 0.1) is None

    def test_cdp_sync_dismiss_alert(self, setup_env):
        alert = synchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert synchronous.dismiss_alert(setup_env, alert) is None

    def test_cdp_sync_dismiss_alert_fails_if_no_alert(self, setup_env):
        no_alert = synchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert synchronous.dismiss_alert(setup_env, no_alert, 0.1) is None

    def test_cdp_sync_get_alert_text(self, setup_env):
        alert = synchronous.find_element(setup_env, By.ID, "alert-button")
        assert synchronous.get_alert_text(setup_env, alert) == "any warn"

    def test_cdp_sync_take_screenshot_of_element(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "button")
        assert synchronous.take_screenshot_element(setup_env, element) is None

    def test_cdp_sync_take_screenshot_of_page(self, setup_env):
        assert synchronous.take_screenshot(setup_env) is None

    def test_cdp_sync_get_computed_label(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "button")
        assert synchronous.get_computed_label(setup_env, element) == "test"

    def test_cdp_sync_get_computed_role(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "button")
        assert synchronous.get_computed_role(setup_env, element) == "button"

    def test_cdp_sync_get_tag_name(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "button")
        assert synchronous.get_tag_name(setup_env, element) == "BUTTON"

    def test_cdp_sync_get_rect(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "button")
        synchronous.set_window_rectangle(setup_env, 100, 100, 0, 0)
        assert synchronous.get_rect(setup_env, element) is not None

    def test_cdp_sync_actions_move_to_element(self, setup_env):
        element = synchronous.find_element(setup_env, By.CSS_SELECTOR, "div.tooltip")
        assert synchronous.actions_move_to_element(setup_env, element) is None

    def test_cdp_sync_actions_scroll_to_element(self, setup_env):
        element = synchronous.find_element(setup_env, By.ID, "alert-button-other")
        assert synchronous.actions_scroll_to_element(setup_env, element) is None

    def test_cdp_sync_submit_form(self, setup_env):
        element = synchronous.find_element(setup_env, By.NAME, "my-form")
        synchronous.actions_scroll_to_element(setup_env, element)
        assert synchronous.submit(setup_env, element) is None

    def test_cdp_sync_find_children_elements(self, setup_env):
        parent_element = synchronous.find_element(setup_env, By.XPATH, '//div[@class="parent"]')
        actual = synchronous.find_children_elements(setup_env, parent_element, By.XPATH, "//div")
        assert len(actual) > 0

    @mark.parametrize(
        "locator",
        [
            (By.CSS_SELECTOR, "div.parent"),
            (By.ID, "parent"),
            (By.TAG_NAME, "p"),
            (By.CLASS_NAME, "parent"),
            (By.XPATH, '//div[@class="parent"]'),
            (By.NAME, "parent"),
            (By.PARTIAL_LINK_TEXT, "parent"),
            (By.LINK_TEXT, "parent.com\n        "),
        ],
    )
    def test_cdp_sync_find_child_element(self, setup_env, locator: Tuple):
        parent_element = synchronous.find_element(setup_env, *locator)
        actual = synchronous.find_child_element(
            setup_env, parent_element, By.XPATH, '//div[@class="child4"]'
        )
        assert synchronous.get_text(setup_env, actual) == "any4"

    def test_cdp_sync_get_page_source(self, setup_env):
        assert "body" in synchronous.get_page_source(setup_env)

    def test_cdp_sync_execute_script(self, setup_env):
        script = "style.background='#000000'"
        element = synchronous.find_element(setup_env, By.XPATH, "//body")
        assert synchronous.execute_script(setup_env, element, script) is not None

    def test_cdp_sync_get_active_element(self, setup_env):
        element = synchronous.find_element(setup_env, By.XPATH, "//input")
        synchronous.send_keys(setup_env, element, "any")
        active = synchronous.get_active_element(setup_env)
        assert synchronous.get_tag_name(setup_env, active) == "INPUT"

    def test_cdp_sync_clear_element(self, setup_env):
        element = synchronous.find_element(setup_env, By.XPATH, "//input")
        synchronous.send_keys(setup_env, element, "any")
        assert synchronous.clear_element(setup_env, element) is None

    def test_cdp_sync_is_enabled(self, setup_env):
        element = synchronous.find_element(setup_env, By.XPATH, "//button")
        assert synchronous.is_element_enabled(setup_env, element) is True

    def test_cdp_sync_get_window_rectangle(self, setup_env):
        synchronous.set_window_rectangle(setup_env, 100, 100, 1, 2)
        assert synchronous.get_window_rectangle(setup_env) is not None

    #
    # def test_cdp_sync_close_window(self, setup_env):
    #
    #         synchronous.new_window(setup_env)
    #         assert synchronous.close_window(setup_env) is None

    def test_cdp_sync_get_window_handler(self, setup_env):
        assert synchronous.get_window(setup_env) is not None

    def test_cdp_sync_get_status(self, setup_env):
        assert synchronous.get_status(setup_env) == {"ready": True}
