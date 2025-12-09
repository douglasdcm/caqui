# It opens the WebDriver, navigate to a page and get all links
# Run `export PYTHONPATH=$(pwd)` before execute it
# python samples/sample-web-driver.py 
# Link found 'http://any1.com/'
# Link found 'http://any2.com/'
# Link found 'http://any3.com/'
# Link found 'http://any4.com/'
# Time: 1.10 sec
import asyncio
import time
from tests.constants import PAGE_URL
from caqui.easy.capabilities import BaseCapabilitiesBuilder, ChromeCapabilitiesBuilder
from caqui.easy.server import LocalServer
from caqui.easy.drivers import AsyncDriver

async def get_all_links(server):
    capabilities: BaseCapabilitiesBuilder = (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .page_load_strategy("normal")
    )

    driver = AsyncDriver("http://localhost:9998",capabilities)

    await driver.get(
        PAGE_URL,
    )

    all_anchors = []
    for i in range(4):
        i += 1
        anchors = await _get_links(driver, i)
        all_anchors.extend(anchors)

    for anchor in all_anchors:
        text = await anchor.get_property("href")
        print(f"Link found '{text}'")

    await driver.close()


async def _get_links(driver, i):
    locator_value = f"//a[@id='a{i}']"
    locator_type = "xpath"
    anchors = []
    anchors = await driver.find_elements(locator_type, locator_value)
    return anchors


try:
    server = LocalServer(port=9998)
    server.start_chrome()
    start = time.time()
    asyncio.run(get_all_links(server))
finally:
    end = time.time()
    print(f"Time: {end-start:.2f} sec")
    server.dispose()
