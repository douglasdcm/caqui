import pytest_asyncio
from aiohttp import ClientSession
from pytest import mark

from caqui.by import By
from caqui.webdriver.capabilities import ChromeCapabilitiesBuilder
from caqui.webdriver.drivers import AsyncDriver
from caqui.webdriver.engine import synchronous

# from caqui.easy.options import ChromeOptionsBuilder
from tests.constants import PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
CAPTURES = "captures"
LOAD = 10  # requests


@mark.skip(reason="Used for performance tests")
class TestPerformance:
    def _build_capabilities(self):
        capabilities = (
            ChromeCapabilitiesBuilder()
            .accept_insecure_certs(True)
            .page_load_strategy("eager")
            .args(["headless"])
        )
        return capabilities

    async def _body(self, driver: AsyncDriver):
        await driver.implicitly_wait(10)
        await driver.get(
            PAGE_URL,
        )
        for _ in range(LOAD):
            click_button = await driver.find_element(By.ID, "button")
            await click_button.click()

        await driver.switch_to.active_element.get_attribute("value")
        element = await driver.find_element(By.XPATH, "//a")
        # Returns and base64 encoded string into image
        await element.screenshot("/tmp/image.png")

        await driver.back()
        await driver.forward()
        await driver.refresh()

        alert_element = await driver.find_element(By.CSS_SELECTOR, "#alert-button-prompt")
        await alert_element.click()
        alert_object = driver.switch_to.alert
        await driver.alert.accept()

        await alert_element.click()
        await alert_object.send_keys("Caqui")
        await alert_object.dismiss()

        iframe = await driver.find_element(By.ID, "my-iframe")
        # switch to selected iframe
        await driver.switch_to.frame(iframe)
        await driver.switch_to.default_content()
        # switching to second iframe based on index
        iframe = (await driver.find_elements(By.ID, "my-iframe"))[0]

        # switch to selected iframe
        await driver.switch_to.frame(iframe)
        # switch back to default content
        await driver.switch_to.default_content()

        window_handle = driver.current_window_handle
        assert len(driver.window_handles) >= 1
        await driver.switch_to.window(window_handle)
        # Opens a new tab and switches to new tab
        await driver.switch_to.new_window("tab")
        # Opens a new window and switches to new window
        await driver.switch_to.new_window("window")

        # Access each dimension individually
        await driver.set_window_size(1024, 768)
        # Move the window to the top left of the primary monitor
        await driver.set_window_position(0, 0)
        await driver.maximize_window()
        # await driver.minimize_window()  # does not work on headless mode
        await driver.save_screenshot("/tmp/image.png")

        # Executing JavaScript to capture innerText of header element
        await driver.execute_script('alert("any warn")')

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
