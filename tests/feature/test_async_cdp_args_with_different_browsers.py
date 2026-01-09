from pytest import fixture, mark

from caqui.cdp.by import By
from caqui.constants import Specification
from caqui.easy.capabilities import (
    ChromeCapabilitiesBuilder,
    EdgeCapabilitiesBuilder,
    FirefoxCapabilitiesBuilder,
    OperaCapabilitiesBuilder,
)
from caqui.easy.cdp.asynchronous.drivers import AsyncDriverCDP
from caqui.easy.server import LocalServer
from tests.constants import PAGE_URL

CAPABILITIES = {
    Specification.CHROME: {
        "capability": ChromeCapabilitiesBuilder().args(["headless"]),
        "port": 9997,
        "url": "http://localhost:9997",
    },
    Specification.FIREFOX: {
        "capability": FirefoxCapabilitiesBuilder().args(["headless"]),
        "port": 9996,
        "url": "http://localhost:9996",
    },
    Specification.OPERA: {
        "capability": OperaCapabilitiesBuilder().args(["headless"]),
        "port": 9995,
        "url": "http://localhost:9995",
    },
    Specification.EDGE: {
        "capability": EdgeCapabilitiesBuilder().args(["headless"]),
        "port": 9994,
        "url": "http://localhost:9994",
    },
}


@mark.skip(reason="Used for local tests")
class TestArgs:
    @fixture(autouse=True, scope="class")
    def setup_server_chrome(self):
        server = LocalServer(CAPABILITIES[Specification.CHROME]["port"])  # type: ignore
        server.start_chrome()
        yield
        server.dispose()

    @fixture(autouse=True, scope="class")
    def setup_server_firefox(self):
        server = LocalServer(
            CAPABILITIES[Specification.FIREFOX]["port"],  # type: ignore
            executable_path=("/home/douglas/.wdm/drivers/geckodriver/linux64/v0.36.0/geckodriver"),
        )
        server.start_firefox()
        yield
        server.dispose()

    @fixture(autouse=True, scope="class")
    def setup_server_opera(self):
        server = LocalServer(
            CAPABILITIES[Specification.OPERA]["port"],  # type: ignore
            executable_path=(
                "/home/douglas/.wdm/drivers/operadriver/linux64/v.140.0.7339.249/"
                "operadriver_linux64/operadriver"
            ),
        )
        server.start_opera()
        yield
        server.dispose()

    @fixture(autouse=True, scope="class")
    def setup_server_edge(self):
        server = LocalServer(
            CAPABILITIES[Specification.EDGE]["port"],  # type: ignore
            executable_path="/home/douglas/.wdm/drivers/edgedriver/142/msedgedriver",
        )
        server.start_edge()
        yield
        server.dispose()

    @mark.parametrize(
        "capabilities",
        [
            CAPABILITIES[Specification.CHROME],
            CAPABILITIES[Specification.FIREFOX],
            CAPABILITIES[Specification.OPERA],
            CAPABILITIES[Specification.EDGE],
        ],
    )
    @mark.asyncio
    async def test_args_with_many_browsers(self, capabilities):
        driver = None
        try:
            server_url = capabilities["url"]
            capabilities["capability"].args(["headless"])
            driver = AsyncDriverCDP(server_url, capabilities["capability"])
            await driver.get(
                PAGE_URL,
            )
            click_button = await driver.find_element(By.ID, "button")
            await click_button.click()
        finally:
            if driver:
                driver.quit()
