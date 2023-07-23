import time
from caqui.caqui import AsyncDriver
from caqui.by import By
from tests.constants import PAGE_URL
from pytest import mark, fixture
from caqui import synchronous


@fixture
def setup():
    remote = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "name": "webdriver",
            "browserName": "chrome",
            "acceptInsecureCerts": True,
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    driver = AsyncDriver(remote, capabilities, PAGE_URL)
    yield driver
    driver.quit()


@mark.asyncio
async def test_big_scenario(setup: AsyncDriver):
    driver = setup
    remote, session = driver.remote, driver.session
    await driver.implicitly_wait(10)

    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    await driver.get(
        "http://www.google.com",
    )
    cookies = await driver.get_cookies()
    assert cookies == synchronous.get_cookies(remote, session)
    cookie = (await driver.get_cookies())[0]
    cookie["name"] = "other"
    await driver.add_cookie(cookie)
    assert await driver.get_cookies() == synchronous.get_cookies(remote, session)
    assert await driver.get_cookie("other") == synchronous.get_named_cookie(
        remote, session, "other"
    )
    await driver.delete_cookie("other")
    await driver.delete_all_cookies()
    assert await driver.get_cookies() == synchronous.get_cookies(remote, session)
    await driver.get(
        PAGE_URL,
    )

    await driver.switch_to.active_element.get_attribute("value")
    element = await driver.find_element(By.XPATH, "//button")
    # Returns and base64 encoded string into image
    await element.screenshot("/tmp/image.png")

    assert await element.is_enabled() == synchronous.is_element_enabled(
        remote, session, element
    )
    assert await element.is_selected() == synchronous.is_element_selected(
        remote, session, element
    )
    assert element.tag_name == synchronous.get_tag_name(remote, session, element)
    assert element.rect == synchronous.get_rect(remote, session, element)
    css = "background-color"
    assert await element.value_of_css_property(css) == synchronous.get_css_value(
        remote, session, element, css
    )
    assert element.text == synchronous.get_text(remote, session, element)
    assert await element.get_attribute("value") == synchronous.get_attribute(
        remote, session, element, "value"
    )
    await driver.back()
    await driver.forward()
    await driver.refresh()

    alert_element = await driver.find_element(By.CSS_SELECTOR, "#alert-button-prompt")
    await alert_element.click()
    alert_object = driver.switch_to.alert
    assert alert_object.text == synchronous.get_alert_text(remote, session)
    await driver.alert.accept()

    await alert_element.click()
    await alert_object.send_keys("Caqui")
    await alert_object.dismiss()

    iframe = await driver.find_element(By.ID, "my-iframe")
    # switch to selected iframe
    await driver.switch_to.frame(iframe)
    await driver.switch_to.default_content()
    # switching to second iframe based on index
    iframe = (await driver.find_elements(By.ID, "my-iframe"))[0]

    # switch to selected iframe
    await driver.switch_to.frame(iframe)
    # switch back to default content
    await driver.switch_to.default_content()

    window_handle = driver.current_window_handle
    assert len(driver.window_handles) >= 1
    driver.switch_to.window(window_handle)
    # Opens a new tab and switches to new tab
    await driver.switch_to.new_window("tab")
    # Opens a new window and switches to new window
    await driver.switch_to.new_window("window")
    # Close the tab or window
    await driver.close()

    # Access each dimension individually
    assert (await driver.get_window_size()).get(
        "width"
    ) == synchronous.get_window_rectangle(remote, session).get("width")
    assert (await driver.get_window_size()).get(
        "height"
    ) == synchronous.get_window_rectangle(remote, session).get("height")

    await driver.set_window_size(1024, 768)
    # Access each dimension individually
    assert (await driver.get_window_position()).get(
        "x"
    ) == synchronous.get_window_rectangle(remote, session).get("x")

    assert (await driver.get_window_position()).get("y") == (
        synchronous.get_window_rectangle(remote, session)
    ).get("y")

    # Move the window to the top left of the primary monitor
    await driver.set_window_position(0, 0)
    await driver.maximize_window()
    await driver.minimize_window()
    await driver.save_screenshot("/tmp/image.png")

    # Executing JavaScript to capture innerText of header element
    await driver.execute_script('alert("any warn")')
