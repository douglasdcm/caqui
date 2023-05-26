import asyncio
import time
from caqui import synchronous, asynchronous

from os import getcwd

BASE_DIR = getcwd()
ROOT_DIR = BASE_DIR + "/caqui/src"
TEST_DIR = BASE_DIR + "/tests"


async def get_all_links():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
        }
    }
    comp_data = [
        {
            "page": f"https://www.dqrtech.com.br/vagas/",
            "locator": f"//a[contains(@title,'Veja detalhes')]",
        },
        {
            "page": f"https://ciandt.com/us/en-us/careers/open-positions",
            "locator": "//a[contains(@class,'wp-block-cit-block-ciandt-link')]",
        },
    ]

    for data in comp_data:
        session = await asynchronous.get_session(driver_url, capabilities)
        await asynchronous.go_to_page(
            driver_url,
            session,
            data["page"],
        )

        locator_type = "xpath"
        anchors = []

        anchors = await asynchronous.find_elements(
            driver_url, session, locator_type, data["locator"]
        )
        print(f"Found {len(anchors)} links")
        for anchor in anchors:
            text = await asynchronous.get_property(driver_url, session, anchor, "href")
            print(f"Link found '{text}'")

        synchronous.close_session(driver_url, session)


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        get_all_links(),
        get_all_links(),
        get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
        # get_all_links(),
    )


start = time.time()

asyncio.run(main())

end = time.time()
print(f"Time: {end-start:.2f} sec")
