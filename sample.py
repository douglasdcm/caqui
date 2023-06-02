import asyncio
import time
from caqui import synchronous, asynchronous
from os import getcwd
from tests.constants import PAGE_URL

BASE_DIR = getcwd()

MAX_CONCURRENCY = 5  # number of webdriver instances running
sem = asyncio.Semaphore(MAX_CONCURRENCY)


async def get_all_links():
    async with sem:
        driver_url = "http://127.0.0.1:9999"
        capabilities = {
            "desiredCapabilities": {
                "browserName": "firefox",
                "marionette": True,
                "acceptInsecureCerts": True,
            }
        }

        session = await asynchronous.get_session(driver_url, capabilities)
        await asynchronous.go_to_page(
            driver_url,
            session,
            PAGE_URL,
        )

        for i in range(4):
            i += 1
            locator_value = f"//a[@id='a{i}']"
            locator_type = "xpath"
            anchors = []

            anchors = await asynchronous.find_elements(
                driver_url, session, locator_type, locator_value
            )
            print(f"Found {len(anchors)} links")

        for anchor in anchors:
            text = await asynchronous.get_property(driver_url, session, anchor, "href")
            print(f"Link found '{text}'")

        synchronous.close_session(driver_url, session)


# Reference: https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
async def main():
    number_of_websites = range(10)
    tasks = [asyncio.ensure_future(get_all_links()) for number in number_of_websites]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        end = time.time()
        print(f"Time: {end-start:.2f} sec")
