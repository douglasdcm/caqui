# It opens the WebDriver, navigate to a page and get all links
import asyncio
import time
from caqui import synchronous, asynchronous
from caqui.easy.options import ChromeOptionsBuilder
from tests.constants import PAGE_URL
from caqui.easy.capabilities import BaseCapabilities, ChromeCapabilitiesBuilder
from caqui.easy.server import Server


async def get_all_links(server):
    server_url = server.url
    options = ChromeOptionsBuilder().args(["headless"]).to_dict()
    capabilities: BaseCapabilities = (
        ChromeCapabilitiesBuilder()
        .accept_insecure_certs(True)
        .page_load_strategy("normal")
        .add_options(options)
    ).to_dict()

    session = await asynchronous.get_session(server_url, capabilities)
    await asynchronous.go_to_page(
        server_url,
        session,
        PAGE_URL,
    )

    all_anchors = []
    for i in range(4):
        i += 1
        anchors = await __get_links(server_url, session, i)
        all_anchors.extend(anchors)

    for anchor in all_anchors:
        text = await asynchronous.get_property(server_url, session, anchor, "href")
        print(f"Link found '{text}'")

    synchronous.close_session(server_url, session)


async def __get_links(server_url, session, i):
    locator_value = f"//a[@id='a{i}']"
    locator_type = "xpath"
    anchors = []
    anchors = await asynchronous.find_elements(server_url, session, locator_type, locator_value)
    return anchors


try:
    server = Server(port=9998)
    server.start()
    start = time.time()
    asyncio.run(get_all_links(server))
finally:
    end = time.time()
    print(f"Time: {end-start:.2f} sec")
    server.dispose()
