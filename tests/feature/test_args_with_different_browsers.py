import pytest_asyncio
from aiohttp import ClientSession
from pytest import mark

from caqui import synchronous
from caqui.by import By
from caqui.easy import AsyncPage
from caqui.easy.capabilities import (
    ChromeCapabilitiesBuilder,
    FirefoxCapabilitiesBuilder,
    EdgeCapabilitiesBuilder,
)
from caqui.easy.options import ChromeOptionsBuilder, FirefoxOptionsBuilder, EdgeOptionsBuilder
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"


# @mark.skip(reason="Used for performance tests")
class TestArgs:
    def _build_capabilities(self):
        capabilities = []
        # options = ChromeOptionsBuilder().with_headless().with_speed_flags()
        # chrome_capabilities = (
        #     ChromeCapabilitiesBuilder()
        #     .accept_insecure_certs(True)
        #     .add_options(options)
        #     .page_load_strategy("eager")
        # )
        # capabilities.append(chrome_capabilities)

        options = FirefoxOptionsBuilder().with_headless().with_speed_flags()
        options = FirefoxOptionsBuilder().args(["-headless", "-profile"])
        firefox_capabilities = FirefoxCapabilitiesBuilder()
        firefox_capabilities.add_options(options.to_dict())
        capabilities.append(firefox_capabilities)

        # options = EdgeOptionsBuilder().with_headless().with_speed_flags()
        # edge_capabilities = (
        #     EdgeCapabilitiesBuilder()
        #     .accept_insecure_certs(True)
        #     .add_options(options)
        #     .page_load_strategy("eager")
        # )
        # capabilities.append(edge_capabilities)
        return capabilities

    @pytest_asyncio.fixture
    async def setup_environment(self):
        server_url = SERVER_URL
        capabilities = self._build_capabilities()
        for capability in capabilities:
            print(capability)
            page = AsyncPage(server_url, capability, PAGE_URL)
            yield page
            try:
                synchronous.dismiss_alert(server_url, page.session)
            except Exception:
                pass
            finally:
                page.quit()

    @mark.asyncio
    async def test_args_with_many_browsers(
        self,
        setup_environment: AsyncPage,
    ):
        page = setup_environment
        await page.implicitly_wait(10)
        await page.get(
            PAGE_URL,
        )
        click_button = await page.find_element(By.ID, "button")
        await click_button.click()
