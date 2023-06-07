import asyncio
import time
from caqui import synchronous, asynchronous
from os import getcwd
from tests.constants import PAGE_URL

BASE_DIR = getcwd()

MAX_CONCURRENCY = 5  # number of webdriver instances running
all_anchors = []


def main():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "capabilities": {"firstMatch": [{}], "alwaysMatch": {}},
        "desiredCapabilities": {
            "debugConnectToRunningApp": "false",
            "app": "C:/windows/system32/calc.exe",
        },
    }
    session = synchronous.get_session(driver_url, capabilities)
    element = synchronous.find_element(
        driver_url, session, locator_type="name", locator_value="Eight"
    )

    synchronous.click(driver_url, session, element)
    synchronous.close_session(driver_url, session)


if __name__ == "__main__":
    main()
