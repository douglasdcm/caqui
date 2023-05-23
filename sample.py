import asyncio
import time
from caqui import synchronous, asynchronous

from os import getcwd

BASE_DIR = getcwd()
ROOT_DIR = BASE_DIR + "/caqui/src"
TEST_DIR = BASE_DIR + "/tests"

PAGE_URL = f"file:///{TEST_DIR}/html/playground.html"


async def get_all_links():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
        }
    }
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )

    locator_type = "xpath"
    anchors = []

    for i in range(4):
        i += 1
        locator_value = f"//a[@id='a{i}']"
        anchor = synchronous.find_element(
            driver_url, session, locator_type, locator_value
        )
        anchors.append(anchor)
        assert (
            await asynchronous.get_text(driver_url, session, anchors[i - 1])
            == f"any{i}.com"
        )

    synchronous.close_session(driver_url, session)


start = time.time()

loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
    loop.create_task(get_all_links()),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

end = time.time()
print(f"Time: {end-start:.2f} sec")
