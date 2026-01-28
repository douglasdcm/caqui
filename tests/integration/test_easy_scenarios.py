from pytest import mark

from caqui.by import By
from caqui.webdriver.capabilities import ChromeCapabilitiesBuilder
from caqui.webdriver.drivers import AsyncDriver
from caqui.webdriver.engine import synchronous

# from caqui.easy.options import ChromeOptionsBuilder
from tests.constants import COOKIE, PAGE_URL

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"


def test_async_driver_nested_capabilities():
    expected = {
        "desiredCapabilities": {
            "browserName": "any",
            "goog:chromeOptions": {
                "args": ["headless"],
                "prefs": {"javascript.options.showInConsole": False},
                "detach": True,
                "binary": "/path/to/chrome/executable",
                "extensions": ["ext1", "ext2"],
                "localState": {"any": "any"},
                "debuggerAddress": "127.0.0.1:9999",
                "excludeSwitches": ["sw1", "sw2"],
                "minidumpPath": "any",
                "mobileEmulation": {"any": "any"},
                "windowsTypes": ["any"],
                "perfLoggingPrefs": {
                    "enableNetwork": False,
                    "enablePage": False,
                    "traceCategories": "devtools.network",
                    "bufferUsageReportingInterval": 1000,
                },
            },
        }
    }

    capabilities = ChromeCapabilitiesBuilder()
    (
        capabilities.browser_name("any")
        .args(["headless"])
        .prefs({"javascript.options.showInConsole": False})
        .detach(True)
        .binary("/path/to/chrome/executable")
        .extensions(["ext1", "ext2"])
        .local_state({"any": "any"})
        .debugger_address("127.0.0.1:9999")
        .exclude_switches(["sw1", "sw2"])
        .minidump_path("any")
        .mobile_emulation({"any": "any"})
        .windows_types(["any"])
        .perf_logging_prefs(
            {
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
                "bufferUsageReportingInterval": 1000,
            }
        )
    )

    assert capabilities.to_dict() == expected


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(setup_environment: AsyncDriver):
    driver = setup_environment
    await driver.get(PAGE_URL)

    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.scroll_to_element(element_form).perform()
    element_frame = await driver.find_element(locator_type, locator_value)
    await driver.switch_to.frame(element_frame)

    alert_button_frame = await driver.find_element(locator_type, locator_value_alert_frame)
    await alert_button_frame.click()
    await driver.switch_to.alert.dismiss()

    await driver.switch_to.default_content()
    alert_button_parent = await driver.find_element(locator_type, locator_value_alert_parent)
    assert await alert_button_parent.get_attribute("any") == "any"
    await alert_button_parent.click()


@mark.asyncio
async def test_switch_to_frame_and_click_alert(setup_environment: AsyncDriver):
    driver = setup_environment
    await driver.get(PAGE_URL)
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.move_to_element(element_form).perform()

    element_frame = await driver.find_element(locator_type, locator_value)
    await driver.switch_to.frame(element_frame)

    alert_button = await driver.find_element(locator_type, locator_value_alert)
    assert await alert_button.get_attribute("any") == "any"
    await alert_button.click()


@mark.asyncio
async def test_get_data_from_hidden_button(setup_environment: AsyncDriver):
    driver = setup_environment
    locator_type = "xpath"
    await driver.get(PAGE_URL)

    hidden_button = await driver.find_element(locator_type, "//*[@id='hidden-button']")

    assert "width" in await hidden_button.get_rect()
    assert "visible" == await hidden_button.get_css_value("visibility")
    assert True is await hidden_button.get_property("hidden")
    assert "display" in await hidden_button.get_property("style")
    assert "display: none;" in await hidden_button.get_attribute("style")


@mark.asyncio
async def test_add_text__click_button_and_get_properties(setup_environment: AsyncDriver):
    driver = setup_environment
    expected = "end"
    locator_type = "xpath"
    await driver.get(PAGE_URL)

    input_ = await driver.find_element(locator_type, "//input")
    await input_.send_keys("any")
    assert await input_.get_property("value") == "any"
    await input_.clear()
    assert await input_.get_property("value") == ""

    anchor = await driver.find_element(locator_type, "//a")
    assert "http://any1.com" in await anchor.get_property("href")

    button = await driver.find_element(locator_type, "//button")
    await button.click()

    p = await driver.find_element(locator_type, "//p[@id='end']")

    assert await p.get_text() == expected


@mark.asyncio
async def test_big_scenario_of_functions(setup_environment: AsyncDriver):
    driver = setup_environment
    server_url, session = driver.server_url, driver.session
    await driver.implicitly_wait(10)

    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    await driver.get(
        "https://example.org/",
    )
    cookies = COOKIE
    await driver.add_cookie(cookies)
    assert cookies.get("domain") == synchronous.get_cookies(server_url, session)[0].get("domain")
    cookie = (await driver.get_cookies())[0]
    cookie["name"] = "other"
    await driver.add_cookie(cookie)
    assert await driver.get_cookies() == synchronous.get_cookies(server_url, session)
    assert await driver.get_cookie("other") == synchronous.get_named_cookie(
        server_url, session, "other"
    )
    await driver.delete_cookie("other")
    await driver.delete_all_cookies()
    assert await driver.get_cookies() == synchronous.get_cookies(server_url, session)
    await driver.get(
        PAGE_URL,
    )

    await driver.switch_to.active_element.get_attribute("value")
    element = await driver.find_element(By.XPATH, "//a")
    # Returns and base64 encoded string into image
    await element.screenshot("/tmp/image.png")

    assert await element.is_enabled() == synchronous.is_element_enabled(
        server_url, session, element.element_id
    )
    assert await element.is_selected() == synchronous.is_element_selected(
        server_url, session, element.element_id
    )
    assert element.tag_name == synchronous.get_tag_name(server_url, session, element.element_id)
    assert element.rect == synchronous.get_rect(server_url, session, element.element_id)
    css = "background-color"
    assert await element.value_of_css_property(css) == synchronous.get_css_value(
        server_url, session, element.element_id, css
    )
    assert element.text == synchronous.get_text(server_url, session, element.element_id)
    assert await element.get_attribute("value") == synchronous.get_attribute(
        server_url, session, element.element_id, "value"
    )
    await driver.back()
    await driver.forward()
    await driver.refresh()

    alert_element = await driver.find_element(By.CSS_SELECTOR, "#alert-button-prompt")
    await alert_element.click()
    alert_object = driver.switch_to.alert
    assert alert_object.text == synchronous.get_alert_text(server_url, session)
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
    await driver.switch_to.window(window_handle)
    # Opens a new tab and switches to new tab
    await driver.switch_to.new_window("tab")
    # Opens a new window and switches to new window
    await driver.switch_to.new_window("window")

    # Access each dimension individually
    assert (await driver.get_window_size()).get("width") == synchronous.get_window_rectangle(
        server_url, session
    ).get("width")
    assert (await driver.get_window_size()).get("height") == synchronous.get_window_rectangle(
        server_url, session
    ).get("height")

    await driver.set_window_size(1024, 768)
    # Access each dimension individually
    assert (await driver.get_window_position()).get("x") == synchronous.get_window_rectangle(
        server_url, session
    ).get("x")

    assert (await driver.get_window_position()).get("y") == (
        synchronous.get_window_rectangle(server_url, session)
    ).get("y")

    # Move the window to the top left of the primary monitor
    await driver.set_window_position(0, 0)
    await driver.maximize_window()
    # await driver.minimize_window()  # does not work on headless mode
    await driver.save_screenshot("/tmp/image.png")

    # Executing JavaScript to capture innerText of header element
    await driver.execute_script('alert("any warn")')
    await driver.alert.dismiss()
