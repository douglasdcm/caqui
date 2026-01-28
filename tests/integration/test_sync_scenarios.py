from pytest import mark

from caqui.webdriver.drivers import AsyncDriver


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert_foo(setup_playground: AsyncDriver):
    driver = setup_playground
    locator = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.scroll_to_element(element_form, delta_y=1000).perform()
    element_frame = await driver.find_element(locator, locator_value)
    await driver.switch_to.frame(element_frame)

    alert_button_frame = await driver.find_element(locator, locator_value_alert_frame)
    await alert_button_frame.click()
    await driver.alert.dismiss()
    await driver.switch_to.default_content()

    alert_button_parent = await driver.find_element(locator, locator_value_alert_parent)
    assert await alert_button_parent.get_attribute("any") == "any"
    await alert_button_parent.click()


@mark.asyncio
async def test_switch_to_frame_and_click_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.move_to_element(element_form).perform()
    element_frame = await driver.find_element(locator, locator_value)
    await driver.switch_to.frame(element_frame)

    alert_button = await driver.find_element(locator, locator_value_alert)
    assert await alert_button.get_attribute("any") == "any"
    await alert_button.click()


@mark.asyncio
async def test_get_data_from_hidden_button(setup_playground: AsyncDriver):
    driver = setup_playground
    locator = "xpath"

    hidden_button = await driver.find_element(locator, value="//*[@id='hidden-button']")
    r = await hidden_button.get_rect()
    assert "width" in r.keys()
    assert "visible" == await hidden_button.get_css_value("visibility")
    assert True is await hidden_button.get_property("hidden")
    assert "display" in await hidden_button.get_property("style")
    assert "display: none;" in await hidden_button.get_attribute("style")


@mark.asyncio
async def test_add_text__click_button_and_get_properties(setup_playground: AsyncDriver):
    driver = setup_playground
    expected = "end"
    locator = "xpath"

    input = await driver.find_element(locator, value="//input")
    await input.send_keys("any")
    assert await input.get_property("value") == "any"
    await input.clear()
    assert await input.get_property("value") == ""

    anchor = await driver.find_element(locator, value="//a")
    assert "http://any1.com/" in await anchor.get_property("href")

    button = await driver.find_element(locator, value="//button")
    await button.click()

    p = await driver.find_element(locator, value="//p[@id='end']")

    assert await p.get_text() == expected
