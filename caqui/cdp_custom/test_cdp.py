from pytest import mark, raises
from caqui.cdp_custom.commands import click_element, navigate
from caqui.cdp_custom.launcher import launch_chrome, get_ws_url
from cdp import page
from caqui.cdp_custom.connection import CDPConnection
import websockets

from caqui.exceptions import WebDriverError
from tests.constants import PAGE_URL

@mark.asyncio
async def test_launcher():

    cdp_instance = launch_chrome()
    get_ws_url()
    await navigate("https://manojkumar4636.github.io/Selenium_Practice_Hub/pages/Button.html")
    assert cdp_instance
    await click_element("home")
    cdp_instance.close()

def test_pycdp():
    frame_id = page.FrameId('my id')
    assert repr(frame_id) == "FrameId('my id')"


@mark.asyncio
async def test_pycdp_example():
    # Connect to a Chrome DevTools Protocol endpoint
    # cdp_instance = launch_chrome()
    get_ws_url()
    # Navigate to a URL
    async with CDPConnection(get_ws_url()) as conn:
    # async with websockets.connect(get_ws_url()) as conn:
        assert 42 == await conn.execute(
            page.navigate(url="https://example.com")
        )
        frame_id, loader_id, error = await conn.execute(
            page.navigate(url="https://example.com")
        )
        print(f"Navigated to example.com, frame_id: {frame_id}")


from caqui.cdp_custom import asyncronous

class TestCDPCustom:
    @mark.asyncio
    async def test_cdp_get(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.get(conn, PAGE_URL) is None

    @mark.asyncio
    async def test_cdp_find_element_by_xpath(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, "xpath","//*[@id='input']") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_css_selector(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, "css selector","#input") is not None


    @mark.asyncio
    async def test_cdp_find_element_invalid(self):
        with raises(WebDriverError):
            async with CDPConnection(get_ws_url()) as conn:
                await asyncronous.find_element(conn, "xpath","invalid")


    @mark.asyncio
    async def test_cdp_click(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, "css selector","#button")
            assert await asyncronous.click(conn, element) is None


    # @mark.asyncio
    # async def test_cdp_send_keys(self):
    #     element = await asyncronous.find_element("//*[@id='input']")
    #     assert await asyncronous.send_keys(element) is None
