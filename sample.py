# It opens the WebDriver, navigate to a page and get all links
import asyncio
import time
from caqui import synchronous, asynchronous
from os import getcwd
from tests.constants import PAGE_URL
from caqui.easy.capabilities import CapabilitiesBuilder

BASE_DIR = getcwd()

MAX_CONCURRENCY = 5  # number of webdriver instances running
all_anchors = []
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def get_all_links():
    async with semaphore:
        driver_url = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .page_load_strategy("normal")
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        session = await asynchronous.get_session(driver_url, capabilities)
        await asynchronous.go_to_page(
            driver_url,
            session,
            PAGE_URL,
        )

        all_anchors = []
        for i in range(4):
            i += 1
            locator_value = f"//a[@id='a{i}']"
            locator_type = "xpath"
            anchors = []

            anchors = await asynchronous.find_elements(
                driver_url, session, locator_type, locator_value
            )
            all_anchors.extend(anchors)

        texts = []
        for anchor in all_anchors:
            text = await asynchronous.get_property(driver_url, session, anchor, "href")
            texts.append(text)

        for text in texts:
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
        print(f"Found 40 links")  # 10 websites with 4 links each
        print(f"Time: {end-start:.2f} sec")
