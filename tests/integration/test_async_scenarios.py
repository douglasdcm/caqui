from caqui import synchronous, asynchronous
from tests.constants import PAGE_URL
from pytest import fixture, mark


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    session = synchronous.get_session(driver_url, capabilities)
    synchronous.go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    synchronous.close_session(driver_url, session)


@mark.asyncio
async def test_get_all_links(__setup):
    driver_url, session = __setup
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
