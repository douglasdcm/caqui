import pytest_asyncio
from pytest import mark

from caqui.by import By
from caqui.easy import AsyncDriver
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"


@mark.skip(reason="Used for performance tests")
class TestArgs:
    def _build_capabilities(self):
        capabilities = []
        return capabilities

    @pytest_asyncio.fixture
    async def setup_environment(self):
        server_url = SERVER_URL
        capabilities = self._build_capabilities()
        for capability in capabilities:
            page = AsyncDriver(server_url, capability, PAGE_URL)
            yield page
            page.quit()

    @mark.asyncio
    async def test_args_with_many_browsers(
        self,
        setup_environment: AsyncDriver,
    ):
        page = setup_environment
        await page.implicitly_wait(10)
        await page.get(
            PAGE_URL,
        )
        click_button = await page.find_element(By.ID, "button")
        await click_button.click()
