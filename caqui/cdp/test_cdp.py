from pytest import mark, raises
import pytest_asyncio
from caqui.cdp.commands import click_element, navigate
from caqui.cdp.launcher import close_chrome, launch_chrome, get_ws_url
from cdp import page
from caqui.cdp.connection import CDPConnection
import websockets

from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, PAGE_URL
from caqui.by import By
from caqui.cdp import asyncronous


class TestCDPCustom:
    @pytest_asyncio.fixture(scope="function", autouse=True)
    async def cdp_get(self):
        # launch_chrome()
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.get(conn, PAGE_URL) is None
        yield
        # close_chrome()

    @mark.asyncio
    async def test_cdp_find_element_by_xpath(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.XPATH, "//*[@id='input']") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_css_selector(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.CSS_SELECTOR, "#input") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_id(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.ID, "input") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_class_name(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.CLASS_NAME, "my-class") is not None

    @mark.asyncio
    async def test_cdp_find_element_invalid(self):
        with raises(WebDriverError):
            async with CDPConnection(get_ws_url()) as conn:
                await asyncronous.find_element(conn, By.XPATH, "invalid")

    # TODO get by other locators
    @mark.asyncio
    async def test_cdp_find_elements(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_elements(conn, By.CSS_SELECTOR, "#input") is not None

    @mark.asyncio
    async def test_cdp_click(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.CSS_SELECTOR, "#button")
            assert await asyncronous.click(conn, element) is None

    @mark.asyncio
    async def test_cdp_send_keys(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.XPATH, "//*[@id='input']")
            assert await asyncronous.send_keys(conn, element, text="caqui") is None

    @mark.asyncio
    async def test_cdp_get_text(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "Basic page"
            element = await asyncronous.find_element(conn, By.XPATH, "//h1")
            assert await asyncronous.get_text(conn, element) == expected

    @mark.asyncio
    async def test_cdp_get_attribute_style(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "color: red;"
            element = await asyncronous.find_element(conn, By.ID, "button")
            await asyncronous.click(conn, element)
            assert await asyncronous.get_attribute(conn, element, "style") == expected

    @mark.asyncio
    async def test_cdp_get_attribute_href(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "http://any1.com"
            element = await asyncronous.find_element(conn, By.ID, "a1")
            assert await asyncronous.get_attribute(conn, element, "href") == expected

    @mark.asyncio
    async def test_cdp_get_title(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "Sample page"
            assert await asyncronous.get_title(conn) == expected

    @mark.asyncio
    async def test_cdp_get_url(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "file:///home/douglas/repo/caqui/tests/html/playground.html"
            assert await asyncronous.get_url(conn) == expected

    @mark.asyncio
    async def test_cdp_go_back(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.go_back(conn) is None

    @mark.asyncio
    async def test_cdp_element_is_selected(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.CSS_SELECTOR, "#interest-tech")
            assert await asyncronous.is_element_selected(conn, element) is True

    @mark.asyncio
    async def test_cdp_element_is_not_selected(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.CSS_SELECTOR, "#interest-sports")
            assert await asyncronous.is_element_selected(conn, element) is False

    @mark.asyncio
    async def test_cdp_css_value(self):
        async with CDPConnection(get_ws_url()) as conn:
            expected = "red"
            element = await asyncronous.find_element(conn, By.ID, "button")
            await asyncronous.click(conn, element)
            assert await asyncronous.get_css_value(conn, element, "color") == expected

    @mark.asyncio
    async def test_cdp_handle_cookie(self):
        async with CDPConnection(get_ws_url()) as conn:
            await asyncronous.get(conn, "https://example.org/")
            await asyncronous.add_cookie(conn, COOKIE)
            cookie = await asyncronous.get_named_cookie(conn, COOKIE.get("name"))
            assert cookie.get("name") == COOKIE.get("name")
            assert (
                await asyncronous.delete_cookie(
                    conn, COOKIE.get("name"), COOKIE.get("url"), COOKIE.get("domain")
                )
                is None
            )

    @mark.asyncio
    async def test_cdp_delete_all_cookies(self):
        async with CDPConnection(get_ws_url()) as conn:
            await asyncronous.get(conn, "https://example.org/")
            await asyncronous.add_cookie(conn, COOKIE)
            assert (
                await asyncronous.delete_all_cookies(
                    conn,
                )
                is None
            )

    @mark.asyncio
    async def test_cdp_refresh_page(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.refresh_page(conn) is None

    @mark.asyncio
    async def test_cdp_go_forward(self):
        async with CDPConnection(get_ws_url()) as conn:
            await asyncronous.get(conn, "https://example.org/")
            await asyncronous.go_back(conn)
            assert await asyncronous.go_forward(conn) is None

    @mark.asyncio
    async def test_cdp_set_window_rectangle(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.set_window_rectangle(conn, width=300, height=300) is None

    @mark.asyncio
    async def test_cdp_set_fullscreen(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.fullscreen_window(conn) is None

    @mark.asyncio
    async def test_cdp_minimized(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.minimize_window(conn) is None

    @mark.asyncio
    async def test_cdp_set_maximized(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.maximize_window(conn) is None

    @mark.asyncio
    async def test_cdp_get_window_handlers(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert len(await asyncronous.get_window_handles(conn)) > 0

    @mark.asyncio
    async def test_cdp_new_window(self):
        async with CDPConnection(get_ws_url()) as conn:
            await asyncronous.new_window(conn) is None
            assert len(await asyncronous.get_window_handles(conn)) > 1

    @mark.asyncio
    async def test_cdp_switch_to_window(self):
        async with CDPConnection(get_ws_url()) as conn:
            await asyncronous.new_window(conn) is None
            handle = await asyncronous.get_window_handles(conn)
            assert await asyncronous.switch_to_window(conn, handle[-1]) is None

    @mark.asyncio
    async def test_cdp_switch_to_frame(self):
        async with CDPConnection(get_ws_url()) as conn:
            iframe_id = await asyncronous.find_element(conn, By.ID, "my-iframe")
            iframe_node = await asyncronous.switch_to_frame(conn, iframe_id)
            assert iframe_node is not None

            element = await asyncronous.find_element(
                conn, By.ID, "alert-button-iframe", iframe_node
            )
            assert await asyncronous.get_attribute(conn, element, "any") == "any"

    @mark.asyncio
    async def test_cdp_switch_to_parent_frame(self):
        async with CDPConnection(get_ws_url()) as conn:
            iframe_id = await asyncronous.find_element(conn, By.ID, "my-iframe")
            iframe_node = await asyncronous.switch_to_frame(conn, iframe_id)
            await asyncronous.find_element(conn, By.ID, "alert-button-iframe", iframe_node)
            parent_frame = await asyncronous.switch_to_parent_frame(conn)
            assert parent_frame is not None
            with raises(WebDriverError):
                await asyncronous.find_element(conn, By.ID, "alert-button-iframe", iframe_node)

    @mark.asyncio
    async def test_cdp_send_alert_text(self):
        async with CDPConnection(get_ws_url()) as conn:
            alert = await asyncronous.find_element(conn, By.ID, "alert-button-prompt")
            assert await asyncronous.send_alert_text(conn, alert, "any") is None

    @mark.asyncio
    async def test_cdp_send_alert_text_fails_if_no_alert(self):
        async with CDPConnection(get_ws_url()) as conn:
            no_alert = await asyncronous.find_element(conn, By.ID, "button")
            with raises(WebDriverError):
                assert await asyncronous.send_alert_text(conn, no_alert, "any", 0.1) is None

    @mark.asyncio
    async def test_cdp_accept_alert(self):
        async with CDPConnection(get_ws_url()) as conn:
            alert = await asyncronous.find_element(conn, By.ID, "alert-button-prompt")
            assert await asyncronous.accept_alert(conn, alert) is None

    @mark.asyncio
    async def test_cdp_accept_alert_fails_if_no_alert(self):
        async with CDPConnection(get_ws_url()) as conn:
            no_alert = await asyncronous.find_element(conn, By.ID, "button")
            with raises(WebDriverError):
                assert await asyncronous.accept_alert(conn, no_alert, 0.1) is None

    @mark.asyncio
    async def test_cdp_dismiss_alert(self):
        async with CDPConnection(get_ws_url()) as conn:
            alert = await asyncronous.find_element(conn, By.ID, "alert-button-prompt")
            assert await asyncronous.dismiss_alert(conn, alert) is None

    @mark.asyncio
    async def test_cdp_dismiss_alert_fails_if_no_alert(self):
        async with CDPConnection(get_ws_url()) as conn:
            no_alert = await asyncronous.find_element(conn, By.ID, "button")
            with raises(WebDriverError):
                assert await asyncronous.dismiss_alert(conn, no_alert, 0.1) is None

    @mark.asyncio
    async def test_cdp_take_screenshot_of_element(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.ID, "button")
            assert await asyncronous.take_screenshot_element(conn, element) is None

    @mark.asyncio
    async def test_cdp_take_screenshot_of_page(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.take_screenshot(conn) is None

    @mark.asyncio
    async def test_cdp_get_computed_label(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.ID, "button")
            assert await asyncronous.get_computed_label(conn, element) == "test"
