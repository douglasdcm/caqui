import pytest_asyncio
from aiohttp import ClientSession
from pytest import mark

from caqui import synchronous
from caqui.by import By
from caqui.easy import AsyncDriver
from caqui.easy.capabilities import ChromeCapabilitiesBuilder

# from caqui.easy.options import ChromeOptionsBuilder
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"
LOAD = 1  # requests


@mark.skip(reason="Used for performance tests")
class TestPerformance:
    def _build_capabilities(self):
        # options = ChromeOptionsBuilder().with_headless().with_speed_flags()
        capabilities = (
            ChromeCapabilitiesBuilder()
            .accept_insecure_certs(True)
            .page_load_strategy("eager")
            .args(["headless"])
        )
        return capabilities

    async def _body(self, page: AsyncDriver):
        await page.implicitly_wait(10)
        await page.get(
            PAGE_URL,
        )
        for _ in range(LOAD):
            click_button = await page.find_element(By.ID, "button")
            await click_button.click()

        await page.switch_to.active_element.get_attribute("value")
        element = await page.find_element(By.XPATH, "//a")
        # Returns and base64 encoded string into image
        await element.screenshot("/tmp/image.png")

        await page.back()
        await page.forward()
        await page.refresh()

        alert_element = await page.find_element(By.CSS_SELECTOR, "#alert-button-prompt")
        await alert_element.click()
        alert_object = page.switch_to.alert
        await page.alert.accept()

        await alert_element.click()
        await alert_object.send_keys("Caqui")
        await alert_object.dismiss()

        iframe = await page.find_element(By.ID, "my-iframe")
        # switch to selected iframe
        await page.switch_to.frame(iframe)
        await page.switch_to.default_content()
        # switching to second iframe based on index
        iframe = (await page.find_elements(By.ID, "my-iframe"))[0]

        # switch to selected iframe
        await page.switch_to.frame(iframe)
        # switch back to default content
        await page.switch_to.default_content()

        window_handle = page.current_window_handle
        assert len(page.window_handles) >= 1
        await page.switch_to.window(window_handle)
        # Opens a new tab and switches to new tab
        await page.switch_to.new_window("tab")
        # Opens a new window and switches to new window
        await page.switch_to.new_window("window")

        # Access each dimension individually
        await page.set_window_size(1024, 768)
        # Move the window to the top left of the primary monitor
        await page.set_window_position(0, 0)
        await page.maximize_window()
        # await driver.minimize_window()  # does not work on headless mode
        await page.save_screenshot("/tmp/image.png")

        # Executing JavaScript to capture innerText of header element
        await page.execute_script('alert("any warn")')

    @pytest_asyncio.fixture
    async def setup_environment_without_session_http(self):
        server_url = SERVER_URL
        capabilities = self._build_capabilities()
        page = AsyncDriver(server_url, capabilities)
        yield page
        try:
            synchronous.dismiss_alert(server_url, page.session)
        except Exception:
            pass
        finally:
            page.quit()

    @pytest_asyncio.fixture
    async def setup_environment_with_session_http(self):
        server_url = SERVER_URL
        capabilities = self._build_capabilities()
        async with ClientSession() as session_http:
            page = AsyncDriver(server_url, capabilities, session_http=session_http)
            yield page
            try:
                synchronous.dismiss_alert(server_url, page.session)
            except Exception:
                pass
            finally:
                page.quit()

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http1(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http1(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http2(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http2(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http3(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http3(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http4(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http4(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http5(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http5(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http6(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http6(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http7(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http7(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http8(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http8(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http9(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http9(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_with_session_http10(
        self,
        setup_environment_with_session_http: AsyncDriver,
    ):
        page = setup_environment_with_session_http
        await self._body(page)

    @mark.asyncio
    async def test_big_scenario_of_functions_without_session_http10(
        self,
        setup_environment_without_session_http: AsyncDriver,
    ):
        page = setup_environment_without_session_http
        await self._body(page)
