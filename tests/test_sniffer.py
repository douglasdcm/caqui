#### File used to figure out requests format and parameters ####

from selenium import webdriver
from pytest import fixture, mark
from tests.constants import PAGE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions, wait
from selenium.webdriver.common.alert import Alert
import os
from selenium.webdriver.common.action_chains import ActionChains


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
    # driver.find_element().value_of_css_property()
    yield driver
    driver.quit()


@fixture
def setup_binary():
    homedir = os.path.expanduser("~")
    service = Service(f"/home/douglas/web_drivers/chromedriver.113")
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("window-size=1920,1080")
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(PAGE_URL)

    browser._shadowroot_cls

    yield browser
    # browser.quit()


@mark.skip("used just to discover request data")
def test_action_chains(setup):
    driver = setup

    resource = driver.find_element("xpath", "//button")

    action = ActionChains(driver)
    action.move_to_element(resource)
    action.perform()


@mark.skip("used just to discover request data")
def test_switch_to_frame_sniffer(setup):
    driver = setup
    # Click the link to activate the alert
    import time

    time.sleep(3)
    element = driver.find_element(By.ID, "my-iframe")
    driver.switch_to.frame(element)

    element_alert = driver.find_element(By.ID, "alert-button-iframe")
    element_alert.click()
    time.sleep(3)


@mark.skip("used just to discover request data")
def test_switch_to_frame_sniffer(setup):
    driver = setup
    # Click the link to activate the alert
    import time

    time.sleep(3)
    element = driver.find_element(By.ID, "my-iframe")
    driver.switch_to.frame(element)

    element_alert = driver.find_element(By.ID, "alert-button-iframe")
    element_alert.click()
    time.sleep(3)


@mark.skip("used just to discover request data")
def test_send_text_to_alert(setup):
    driver = setup
    # Click the link to activate the alert
    driver.find_element(By.CSS_SELECTOR, "#alert-button-prompt").click()
    import time

    time.sleep(3)

    # Wait for the alert to be displayed
    # wait.until(expected_conditions.alert_is_present())

    # Store the alert in a variable for reuse
    alert = Alert(driver)
    print("alert ", alert.text)

    # Type your message
    alert.send_keys("Selenium")
    time.sleep(3)

    # Press the OK button
    alert.accept()
    time.sleep(3)


@mark.skip("used just to discover request data")
def test_add_cookie(setup):
    driver = setup
    driver.add_cookie({"name": "firstname", "value": "James"})


@mark.skip("used just to discover request data")
def test_submit(setup):
    driver = setup
    search_button = driver.find_element("name", "my-form")
    search_button.submit()


@mark.skip("used just to discover request data")
def test_sniffer_is_displayed(setup_binary):
    driver = setup_binary
    search_button = driver.find_element("xpath", "//button")
    search_button.is_displayed()


@mark.skip("used just to discover request data")
def test_sniffer_actions_scroll_to_element(setup_binary):
    driver = setup_binary
    search_button = driver.find_element("xpath", "//button")
    ActionChains(driver).scroll_to_element(search_button).perform()


@mark.skip("used just to discover request data")
def test_sniffer_actions_click(setup):
    driver = setup
    search_button = driver.find_element("xpath", "//button")
    ActionChains(driver).click(search_button).perform()


@mark.skip("used just to discover request data")
def test_sniffer_find_children_elements(setup):
    driver = setup
    element = driver.find_element(By.XPATH, '//div[@class="parent"]')
    elements = element.find_elements(By.XPATH, "//div")
    for e in elements:
        print("element_text:", e.text)


@mark.skip("used just to discover request data")
def test_exec_script(setup):
    driver = setup
    assert driver.execute_script("return document.body.scrollHeight") == "any"


@mark.skip("used just to discover request data")
def test_clear(setup):
    driver = setup
    element = driver.find_element("xpath", "//input")
    assert element.clear() == "any"


@mark.skip("used just to discover request data")
def test_back(setup):
    assert setup.back() == "any"


@mark.skip("used just to discover request data")
def test_get_title(setup):
    assert setup.title == "any"


@mark.skip("used just to discover request data")
def test_get_attribute(setup):
    driver = setup
    element = driver.find_element("xpath", "//a")
    assert element.get_property("href") == "any"


@mark.skip("used just to discover request data")
def test_find_elements(setup):
    driver = setup
    actual = driver.find_elements("xpath", "//input")
    assert actual == "any"


@mark.skip("used just to discover request data")
def test_get_attribute_from_input(setup):
    driver = setup
    search_box = driver.find_element("xpath", "//input")
    search_box.send_keys("cat")

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
