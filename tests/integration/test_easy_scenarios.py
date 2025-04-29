from caqui.easy import AsyncPage
from caqui.by import By
from caqui import synchronous
from tests.constants import PAGE_URL
from pytest import mark
from tests.constants import COOKIE


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(setup_environment: AsyncPage):
    driver = setup_environment
    await driver.get(PAGE_URL)

    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button_frame = await driver.find_element(locator_type, locator_value_alert_frame)
    assert await alert_button_frame.click() is True
    assert await driver.switch_to.alert.dismiss() is True

    assert await driver.switch_to.default_content() is True
    alert_button_parent = await driver.find_element(locator_type, locator_value_alert_parent)
    assert await alert_button_parent.get_attribute("any") == "any"
    assert await alert_button_parent.click() is True


@mark.asyncio
async def test_switch_to_frame_and_click_alert(setup_environment: AsyncPage):
    driver = setup_environment
    await driver.get(PAGE_URL)
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button = await driver.find_element(locator_type, locator_value_alert)
    assert await alert_button.get_attribute("any") == "any"
    assert await alert_button.click() is True


@mark.asyncio
async def test_get_data_from_hidden_button(setup_environment: AsyncPage):
    driver = setup_environment
    locator_type = "xpath"
    await driver.get(PAGE_URL)

    hidden_button = await driver.find_element(locator_type, "//*[@id='hidden-button']")

    assert "width" in await hidden_button.get_rect()
    assert "visible" == await hidden_button.get_css_value("visibility")
    assert True is await hidden_button.get_property("hidden")
    assert ["display"] == await hidden_button.get_property("style")
    assert "display: none;" == await hidden_button.get_attribute("style")


@mark.asyncio
async def test_add_text__click_button_and_get_properties(setup_environment: AsyncPage):
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
    assert await anchor.get_property("href") == "http://any1.com/"

    button = await driver.find_element(locator_type, "//button")
    await button.click()

    p = await driver.find_element(locator_type, "//p[@id='end']")

    assert await p.get_text() == expected


@mark.asyncio
async def test_big_scenario_of_functions(setup_environment: AsyncPage):
    page = setup_environment
    remote, session = page.remote, page.session
    await page.implicitly_wait(10)

    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    await page.get(
        "https://example.org/",
    )
    cookies = COOKIE
    await page.add_cookie(cookies)
    assert cookies == synchronous.get_cookies(remote, session)[0]
    cookie = (await page.get_cookies())[0]
    cookie["name"] = "other"
    await page.add_cookie(cookie)
    assert await page.get_cookies() == synchronous.get_cookies(remote, session)
    assert await page.get_cookie("other") == synchronous.get_named_cookie(remote, session, "other")
    await page.delete_cookie("other")
    await page.delete_all_cookies()
    assert await page.get_cookies() == synchronous.get_cookies(remote, session)
    await page.get(
        PAGE_URL,
    )

    await page.switch_to.active_element.get_attribute("value")
    element = await page.find_element(By.XPATH, "//a")
    # Returns and base64 encoded string into image
    await element.screenshot("/tmp/image.png")

    assert await element.is_enabled() == synchronous.is_element_enabled(remote, session, element)
    assert await element.is_selected() == synchronous.is_element_selected(remote, session, element)
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
    await page.back()
    await page.forward()
    await page.refresh()

    alert_element = await page.find_element(By.CSS_SELECTOR, "#alert-button-prompt")
    await alert_element.click()
    alert_object = page.switch_to.alert
    assert alert_object.text == synchronous.get_alert_text(remote, session)
    await page.alert.accept()

    await alert_element.click()
    await alert_object.send_keys("Caqui")
    await alert_object.dismiss()

    iframe = await page.find_element(By.ID, "my-iframe")
    # switch to selected iframe
    await page.switch_to.frame(iframe)
    await page.switch_to.default_content()
    # switching to second iframe based on index
    iframe = (await page.find_elements(By.ID, "my-iframe"))[0]

    # switch to selected iframe
    await page.switch_to.frame(iframe)
    # switch back to default content
    await page.switch_to.default_content()

    window_handle = page.current_window_handle
    assert len(page.window_handles) >= 1
    await page.switch_to.window(window_handle)
    # Opens a new tab and switches to new tab
    await page.switch_to.new_window("tab")
    # Opens a new window and switches to new window
    await page.switch_to.new_window("window")

    # Access each dimension individually
    assert (await page.get_window_size()).get("width") == synchronous.get_window_rectangle(
        remote, session
    ).get("width")
    assert (await page.get_window_size()).get("height") == synchronous.get_window_rectangle(
        remote, session
    ).get("height")

    await page.set_window_size(1024, 768)
    # Access each dimension individually
    assert (await page.get_window_position()).get("x") == synchronous.get_window_rectangle(
        remote, session
    ).get("x")

    assert (await page.get_window_position()).get("y") == (
        synchronous.get_window_rectangle(remote, session)
    ).get("y")

    # Move the window to the top left of the primary monitor
    await page.set_window_position(0, 0)
    await page.maximize_window()
    # await driver.minimize_window()  # does not work on headless mode
    await page.save_screenshot("/tmp/image.png")

    # Executing JavaScript to capture innerText of header element
    await page.execute_script('alert("any warn")')
    await page.alert.dismiss()
