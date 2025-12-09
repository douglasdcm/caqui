from pytest import mark

from caqui.easy.drivers import AsyncDriver
from caqui.synchronous import (
    clear_element,
    click,
    find_element,
    get_attribute,
    get_css_value,
    get_property,
    get_rect,
    get_text,
    send_keys,
)


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert_foo(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.scroll_to_element(element_form, delta_y=1000).perform()
    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button_frame = await driver.find_element(locator_type, locator_value_alert_frame)
    assert await alert_button_frame.click() is True
    assert await driver.alert.dismiss() is True
    assert await driver.switch_to.default_content() is True

    alert_button_parent = await driver.find_element(locator_type, locator_value_alert_parent)
    assert await alert_button_parent.get_attribute("any") == "any"
    assert await alert_button_parent.click() is True


@mark.asyncio
async def test_switch_to_frame_and_click_alert(setup_playground: AsyncDriver):
    driver = setup_playground
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"
    locator_type_form = "css selector"
    locator_form = "body > form"

    element_form = await driver.find_element(locator_type_form, locator_form)
    await driver.actions.move_to_element(element_form).perform()
    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button = await driver.find_element(locator_type, locator_value_alert)
    assert await alert_button.get_attribute("any") == "any"
    assert await alert_button.click() is True


def test_get_data_from_hidden_button(setup_playground):
    driver = setup_playground
    locator_type = "xpath"

    hidden_button = find_element(
        driver.server_url, driver.session, locator_type, locator_value="//*[@id='hidden-button']"
    )

    assert "width" in get_rect(driver.server_url, driver.session, hidden_button)
    assert "visible" == get_css_value(
        driver.server_url, driver.session, hidden_button, "visibility"
    )
    assert True is get_property(driver.server_url, driver.session, hidden_button, "hidden")
    assert "display" in get_property(driver.server_url, driver.session, hidden_button, "style")
    assert "display: none;" in get_attribute(
        driver.server_url, driver.session, hidden_button, "style"
    )


def test_add_text__click_button_and_get_properties(setup_playground):
    driver = setup_playground
    expected = "end"
    locator_type = "xpath"

    input = find_element(driver.server_url, driver.session, locator_type, locator_value="//input")
    send_keys(driver.server_url, driver.session, input, "any")
    assert get_property(driver.server_url, driver.session, input, property_name="value") == "any"
    clear_element(driver.server_url, driver.session, input)
    assert get_property(driver.server_url, driver.session, input, property_name="value") == ""

    anchor = find_element(driver.server_url, driver.session, locator_type, locator_value="//a")
    assert "http://any1.com/" in get_property(
        driver.server_url, driver.session, anchor, property_name="href"
    )

    button = find_element(driver.server_url, driver.session, locator_type, locator_value="//button")
    click(driver.server_url, driver.session, button)

    p = find_element(
        driver.server_url, driver.session, locator_type, locator_value="//p[@id='end']"
    )

    assert get_text(driver.server_url, driver.session, p) == expected
