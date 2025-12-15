from pytest import mark, raises
import pytest_asyncio
from caqui.cdp_custom.commands import click_element, navigate
from caqui.cdp_custom.launcher import close_chrome, launch_chrome, get_ws_url
from cdp import page
from caqui.cdp_custom.connection import CDPConnection
import websockets

from caqui.exceptions import WebDriverError
from tests.constants import PAGE_URL
from caqui.by import By
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
            assert await asyncronous.find_element(conn, By.XPATH,"//*[@id='input']") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_css_selector(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.CSS_SELECTOR,"#input") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_id(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.ID,"input") is not None

    @mark.asyncio
    async def test_cdp_find_element_by_class_name(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_element(conn, By.CLASS_NAME,"my-class") is not None


    @mark.asyncio
    async def test_cdp_find_element_invalid(self):
        with raises(WebDriverError):
            async with CDPConnection(get_ws_url()) as conn:
                await asyncronous.find_element(conn, By.XPATH,"invalid")

    # TODO get by other locators
    @mark.asyncio
    async def test_cdp_find_elements(self):
        async with CDPConnection(get_ws_url()) as conn:
            assert await asyncronous.find_elements(conn, By.CSS_SELECTOR,"#input") is not None


    @mark.asyncio
    async def test_cdp_click(self):
        async with CDPConnection(get_ws_url()) as conn:
            element = await asyncronous.find_element(conn, By.CSS_SELECTOR,"#button")
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