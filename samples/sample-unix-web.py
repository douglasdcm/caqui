# It opens the WebDriver, navigate to a page and get all links
import asyncio
import time
from caqui import synchronous, asynchronous
from os import getcwd
from tests.constants import PAGE_URL
from caqui.easy.capabilities import WebCapabilities, Browser, Server

BASE_DIR = getcwd()

MAX_CONCURRENCY = 5  # number of webdriver instances running
all_anchors = []
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def get_all_links():
    async with semaphore:
        server = Server(port=9998)
        server_url = server.url
        capabilities: WebCapabilities = (
            WebCapabilities()
            .browser_name(Browser.CHROME)
            .accept_insecure_certs(True)
            .page_load_strategy("normal")
            # Reference: https://webdriver.io/docs/capabilities/
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
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
            locator_value = f"//a[@id='a{i}']"
            locator_type = "xpath"
            anchors = []

            anchors = await asynchronous.find_elements(
                server_url, session, locator_type, locator_value
            )
            all_anchors.extend(anchors)

        texts = []
        for anchor in all_anchors:
            text = await asynchronous.get_property(server_url, session, anchor, "href")
            texts.append(text)

        for text in texts:
            print(f"Link found '{text}'")

        synchronous.close_session(server_url, session)


# Reference: https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
async def main():
    number_of_websites = range(10)
    tasks = [asyncio.ensure_future(get_all_links()) for number in number_of_websites]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Python 3.10+
    start = time.time()
    try:
        asyncio.run(main())
    finally:
        end = time.time()
        print(f"Found 40 links")  # 10 websites with 4 links each
        print(f"Time: {end-start:.2f} sec")
