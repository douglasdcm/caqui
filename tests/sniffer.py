from selenium import webdriver
from pytest import fixture, mark
from tests.constants import PAGE_URL


@fixture
def setup():
    desired_capabilities = {
        # 'deviceName': 'Device',
        "deviceName": "Emulator",
        "deviceIpAddress": "127.0.0.1",
        "locale": "en-US",
        "debugCodedUI": False,
        "app": "chromedriver",
    }

    driver = webdriver.Remote(
        command_executor="http://localhost:9999",
        desired_capabilities=desired_capabilities,
    )
    driver.get(PAGE_URL)
    yield driver
    driver.quit()


def test_get_attribute_from_input(setup):
    driver = setup
    search_box = driver.find_element("xpath", "//input")
    search_box.send_keys("cat")

    # data = driver.find_element("xpath", "//input").get_attribute("value")
    data = driver.find_element("xpath", "//input").get_property("value")
    assert data == "cat"


@mark.skip("used just to discover request data")
def test_sniff(setup):
    driver = setup
    search_box = driver.find_element("xpath", "//input")
    search_button = driver.find_element("xpath", "//button")
    end = driver.find_element("xpath", "//p[@id='end']")
    search_box.send_keys("cat")
    search_button.click()
    assert end.text == "end"
