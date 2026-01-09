from typing import Tuple

import pytest_asyncio
from pytest import mark, raises, fixture

from caqui.cdp import asynchronous
from caqui.cdp.by import By
from caqui.cdp.connection import AsyncCDPConnection
from caqui.easy.cdp.server import LocalServerCDP, get_ws_url
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, PAGE_URL


class TestCDPASyncFunctionsBlankPage:
    PORT = 9224

    @fixture(autouse=True, scope="class")
    def launch_browser_(self):
        server = LocalServerCDP(self.PORT)
        server.start_edge()
        yield
        server.dispose()

    @pytest_asyncio.fixture
    async def setup_env(self):
        async with AsyncCDPConnection(get_ws_url()) as conn:
            assert await asynchronous.get(conn, PAGE_URL) is None
            await asynchronous.set_window_rectangle(conn, 1000, 1000, 0, 0)
            yield conn

    @mark.asyncio
    async def test_cdp_async_get_title_from_blank_page(self, setup_env):
        handle = (await asynchronous.get_window_handles(setup_env))[0]
        new_conn = await asynchronous.switch_to_window(setup_env, handle)
        assert await asynchronous.get_title(new_conn) == "about:blank"
    
    @mark.asyncio
    async def test_cdp_async_get_body_from_blank_page(self, setup_env):
        handle = (await asynchronous.get_window_handles(setup_env))[0]
        new_conn = await asynchronous.switch_to_window(setup_env, handle)
        assert await asynchronous.find_element(new_conn, By.TAG_NAME, "body") is not None


class TestCDPAsyncFunctions:
    @pytest_asyncio.fixture
    async def setup_env(self):
        async with AsyncCDPConnection(get_ws_url()) as conn:
            assert await asynchronous.get(conn, PAGE_URL) is None
            await asynchronous.set_window_rectangle(conn, 1000, 1000, 0, 0)
            yield conn

    @mark.asyncio
    async def test_cdp_async_find_element_by_xpath(self, setup_env):
        assert await asynchronous.find_element(setup_env, By.XPATH, "//*[@id='input']") is not None

    @mark.asyncio
    async def test_cdp_async_find_element_by_css_selector(self, setup_env):
        assert await asynchronous.find_element(setup_env, By.CSS_SELECTOR, "#input") is not None

    @mark.asyncio
    async def test_cdp_async_find_element_by_id(self, setup_env):
        assert await asynchronous.find_element(setup_env, By.ID, "input") is not None

    @mark.asyncio
    async def test_cdp_async_find_element_by_class_name(self, setup_env):
        assert await asynchronous.find_element(setup_env, By.CLASS_NAME, "my-class") is not None

    @mark.asyncio
    async def test_cdp_async_find_element_invalid(self, setup_env):
        with raises(WebDriverError):
            await asynchronous.find_element(setup_env, By.XPATH, "invalid")

    # @mark.asyncio
    # async def test_cdp_async_get_shadow_element_v1(self, setup_env):
    #     element = await asynchronous.get_shadow_element_v1(
    #         setup_env, By.ID, "shadow-root", By.ID, "shadow-button"
    #     )
    #     assert await asynchronous.get_tag_name(setup_env, element) == "BUTTON"

    @mark.asyncio
    async def test_cdp_async_get_shadow_element(self, setup_env):
        shadow_element = await asynchronous.find_element(setup_env, By.ID, "shadow-root")
        element = await asynchronous.get_shadow_element(
            setup_env, shadow_element, By.ID, "shadow-button"
        )
        assert await asynchronous.get_tag_name(setup_env, element) == "BUTTON"

    @mark.asyncio
    async def test_cdp_async_get_shadow_elements(self, setup_env):
        shadow_element = await asynchronous.find_element(setup_env, By.ID, "shadow-root")
        element = (
            await asynchronous.get_shadow_elements(
                setup_env, shadow_element, By.ID, "shadow-button"
            )
        )[0]
        assert await asynchronous.get_tag_name(setup_env, element) == "BUTTON"

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
    @mark.asyncio
    async def test_cdp_async_find_elements(self, setup_env, locator: Tuple):
        assert await asynchronous.find_elements(setup_env, *locator) is not None

    @mark.asyncio
    async def test_cdp_async_click_foo(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.CSS_SELECTOR, "#button")
        assert await asynchronous.click(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_send_keys(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.XPATH, "//*[@id='input']")
        assert await asynchronous.send_keys(setup_env, element, text="caqui") is None

    @mark.asyncio
    async def test_cdp_async_get_text(self, setup_env):
        expected = "Basic page"
        element = await asynchronous.find_element(setup_env, By.XPATH, "//h1")
        assert await asynchronous.get_text(setup_env, element) == expected

    @mark.asyncio
    async def test_cdp_async_get_attribute_style(self, setup_env):
        expected = "color: red;"
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        await asynchronous.click(setup_env, element)
        assert await asynchronous.get_attribute(setup_env, element, "style") == expected

    @mark.asyncio
    async def test_cdp_async_get_attribute_href(self, setup_env):
        expected = "http://any1.com"
        element = await asynchronous.find_element(setup_env, By.ID, "a1")
        assert await asynchronous.get_attribute(setup_env, element, "href") == expected

    @mark.asyncio
    async def test_cdp_async_get_title(self, setup_env):
        expected = "Sample page"
        assert await asynchronous.get_title(setup_env) == expected

    @mark.asyncio
    async def test_cdp_async_get_url(self, setup_env):
        expected = "file:///home/douglas/repo/caqui/tests/html/playground.html"
        assert await asynchronous.get_url(setup_env) == expected

    @mark.asyncio
    async def test_cdp_async_go_back(self, setup_env):
        assert await asynchronous.go_back(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_element_is_selected(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.CSS_SELECTOR, "#interest-tech")
        assert await asynchronous.is_element_selected(setup_env, element) is True

    @mark.asyncio
    async def test_cdp_async_element_is_not_selected(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.CSS_SELECTOR, "#interest-sports")
        assert await asynchronous.is_element_selected(setup_env, element) is False

    @mark.asyncio
    async def test_cdp_async_get_css_value(self, setup_env):
        expected = "red"
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        await asynchronous.click(setup_env, element)
        assert await asynchronous.get_css_value(setup_env, element, "color") == expected

    @mark.asyncio
    async def test_cdp_async_handle_cookie(self, setup_env):
        await asynchronous.get(setup_env, "https://example.org/")
        await asynchronous.add_cookie(setup_env, COOKIE)
        cookie = await asynchronous.get_named_cookie(setup_env, COOKIE.get("name"))
        assert cookie.get("name") == COOKIE.get("name")
        assert (
            await asynchronous.delete_cookie(
                setup_env, COOKIE.get("name"), COOKIE.get("url"), COOKIE.get("domain")
            )
            is None
        )

    @mark.asyncio
    async def test_cdp_async_get_cookies(self, setup_env):
        await asynchronous.get(setup_env, "https://example.org/")
        await asynchronous.add_cookie(setup_env, COOKIE)
        actual = await asynchronous.get_cookies(setup_env)
        assert len(actual) > 0

    @mark.asyncio
    async def test_cdp_async_delete_all_cookies(self, setup_env):
        await asynchronous.get(setup_env, "https://example.org/")
        await asynchronous.add_cookie(setup_env, COOKIE)
        assert (
            await asynchronous.delete_all_cookies(
                setup_env,
            )
            is None
        )

    @mark.asyncio
    async def test_cdp_async_refresh_page(self, setup_env):
        assert await asynchronous.refresh_page(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_go_forward(self, setup_env):
        await asynchronous.get(setup_env, "https://example.org/")
        await asynchronous.go_back(setup_env)
        assert await asynchronous.go_forward(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_set_window_rectangle(self, setup_env):
        assert await asynchronous.set_window_rectangle(setup_env, width=300, height=300) is None

    @mark.asyncio
    async def test_cdp_async_set_fullscreen(self, setup_env):
        assert await asynchronous.fullscreen_window(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_minimized(self, setup_env):
        assert await asynchronous.minimize_window(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_set_maximized(self, setup_env):
        assert await asynchronous.maximize_window(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_get_window_handlers(self, setup_env):
        assert len(await asynchronous.get_window_handles(setup_env)) > 0

    @mark.asyncio
    async def test_cdp_async_new_window(self, setup_env):
        await asynchronous.new_window(setup_env) is None
        assert len(await asynchronous.get_window_handles(setup_env)) > 1

    @mark.asyncio
    async def test_cdp_async_switch_to_window_tmp(self, setup_env):
        await asynchronous.get(setup_env, PAGE_URL)
        await asynchronous.new_window(setup_env) is None
        handles = await asynchronous.get_window_handles(setup_env)
        await asynchronous.switch_to_window(setup_env, handles[-1]) is not None

    @mark.asyncio
    async def test_cdp_async_switch_to_frame(self, setup_env):
        iframe_id = await asynchronous.find_element(setup_env, By.ID, "my-iframe")
        iframe_node = await asynchronous.switch_to_frame(setup_env, iframe_id)
        assert iframe_node is not None

        element = await asynchronous.find_element(
            setup_env, By.ID, "alert-button-iframe", iframe_node
        )
        assert await asynchronous.get_attribute(setup_env, element, "any") == "any"

    @mark.asyncio
    async def test_cdp_async_switch_to_parent_frame(self, setup_env):
        iframe_id = await asynchronous.find_element(setup_env, By.ID, "my-iframe")
        iframe_node = await asynchronous.switch_to_frame(setup_env, iframe_id)
        await asynchronous.find_element(setup_env, By.ID, "alert-button-iframe", iframe_node)
        parent_frame = await asynchronous.switch_to_parent_frame(setup_env)
        assert parent_frame is not None
        with raises(WebDriverError):
            await asynchronous.find_element(setup_env, By.ID, "alert-button-iframe")

    @mark.asyncio
    async def test_cdp_async_send_alert_text(self, setup_env):
        alert = await asynchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert await asynchronous.send_alert_text(setup_env, alert, "any") is None

    @mark.asyncio
    async def test_cdp_async_send_alert_text_fails_if_no_alert(self, setup_env):
        no_alert = await asynchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert await asynchronous.send_alert_text(setup_env, no_alert, "any", 0.1) is None

    @mark.asyncio
    async def test_cdp_async_accept_alert(self, setup_env):
        alert = await asynchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert await asynchronous.accept_alert(setup_env, alert) is None

    @mark.asyncio
    async def test_cdp_async_accept_alert_fails_if_no_alert(self, setup_env):
        no_alert = await asynchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert await asynchronous.accept_alert(setup_env, no_alert, 0.1) is None

    @mark.asyncio
    async def test_cdp_async_dismiss_alert(self, setup_env):
        alert = await asynchronous.find_element(setup_env, By.ID, "alert-button-prompt")
        assert await asynchronous.dismiss_alert(setup_env, alert) is None

    @mark.asyncio
    async def test_cdp_async_dismiss_alert_fails_if_no_alert(self, setup_env):
        no_alert = await asynchronous.find_element(setup_env, By.ID, "button")
        with raises(WebDriverError):
            assert await asynchronous.dismiss_alert(setup_env, no_alert, 0.1) is None

    @mark.asyncio
    async def test_cdp_async_get_alert_text(self, setup_env):
        alert = await asynchronous.find_element(setup_env, By.ID, "alert-button")
        assert await asynchronous.get_alert_text(setup_env, alert) == "any warn"

    @mark.asyncio
    async def test_cdp_async_take_screenshot_of_element(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        assert await asynchronous.take_screenshot_element(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_take_screenshot_of_page(self, setup_env):
        assert await asynchronous.take_screenshot(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_get_computed_label(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        assert await asynchronous.get_computed_label(setup_env, element) == "test"

    @mark.asyncio
    async def test_cdp_async_get_computed_role(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        assert await asynchronous.get_computed_role(setup_env, element) == "button"

    @mark.asyncio
    async def test_cdp_async_get_tag_name(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        assert await asynchronous.get_tag_name(setup_env, element) == "BUTTON"

    @mark.asyncio
    async def test_cdp_async_get_rect(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "button")
        await asynchronous.set_window_rectangle(setup_env, 100, 100, 0, 0)
        assert await asynchronous.get_rect(setup_env, element) is not None

    @mark.asyncio
    async def test_cdp_async_actions_move_to_element(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.CSS_SELECTOR, "div.tooltip")
        assert await asynchronous.actions_move_to_element(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_actions_scroll_to_element(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.ID, "alert-button-other")
        assert await asynchronous.actions_scroll_to_element(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_submit_form(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.NAME, "my-form")
        await asynchronous.actions_scroll_to_element(setup_env, element)
        assert await asynchronous.submit(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_find_children_elements(self, setup_env):
        parent_element = await asynchronous.find_element(
            setup_env, By.XPATH, '//div[@class="parent"]'
        )
        actual = await asynchronous.find_children_elements(
            setup_env, parent_element, By.XPATH, "//div"
        )
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
    @mark.asyncio
    async def test_cdp_async_find_child_element(self, setup_env, locator: Tuple):
        parent_element = await asynchronous.find_element(setup_env, *locator)
        actual = await asynchronous.find_child_element(
            setup_env, parent_element, By.XPATH, '//div[@class="child4"]'
        )
        assert await asynchronous.get_text(setup_env, actual) == "any4"

    @mark.asyncio
    async def test_cdp_async_get_page_source(self, setup_env):
        assert "body" in await asynchronous.get_page_source(setup_env)

    @mark.asyncio
    async def test_cdp_async_execute_script(self, setup_env):
        script = "style.background='#000000'"
        element = await asynchronous.find_element(setup_env, By.XPATH, "//body")
        assert await asynchronous.execute_script(setup_env, element, script) is not None

    @mark.asyncio
    async def test_cdp_async_get_active_element(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.XPATH, "//input")
        await asynchronous.send_keys(setup_env, element, "any")
        active = await asynchronous.get_active_element(setup_env)
        assert await asynchronous.get_tag_name(setup_env, active) == "INPUT"

    @mark.asyncio
    async def test_cdp_async_clear_element(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.XPATH, "//input")
        await asynchronous.send_keys(setup_env, element, "any")
        assert await asynchronous.clear_element(setup_env, element) is None

    @mark.asyncio
    async def test_cdp_async_is_enabled(self, setup_env):
        element = await asynchronous.find_element(setup_env, By.XPATH, "//button")
        assert await asynchronous.is_element_enabled(setup_env, element) is True

    @mark.asyncio
    async def test_cdp_async_get_window_rectangle(self, setup_env):
        await asynchronous.set_window_rectangle(setup_env, 100, 100, 1, 2)
        assert await asynchronous.get_window_rectangle(setup_env) is not None

    # @mark.asyncio
    # async def test_cdp_async_close_window(self, setup_env):
    #
    #         await asynchronous.new_window(setup_env)
    #         assert await asynchronous.close_window(setup_env) is None

    @mark.asyncio
    async def test_cdp_async_get_window_handler(self, setup_env):
        assert await asynchronous.get_window(setup_env) is not None

    @mark.asyncio
    async def test_cdp_async_get_status(self, setup_env):
        assert await asynchronous.get_status(setup_env) == {"ready": True}
