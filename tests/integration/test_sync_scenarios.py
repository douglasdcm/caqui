from caqui.synchronous import (clear_element, click, dismiss_alert,
                               find_element, get_attribute, get_css_value,
                               get_property, get_rect, get_text, send_keys,
                               switch_to_frame, switch_to_parent_frame)


def test_switch_to_parent_frame_and_click_alert(setup_playground):
    driver = setup_playground
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = find_element(driver.server_url, driver.session, locator_type, locator_value)
    assert switch_to_frame(driver.server_url, driver.session, element_frame) is True

    alert_button_frame = find_element(
        driver.server_url, driver.session, locator_type, locator_value_alert_frame
    )
    assert click(driver.server_url, driver.session, alert_button_frame) is True
    assert dismiss_alert(driver.server_url, driver.session) is True

    assert switch_to_parent_frame(driver.server_url, driver.session, element_frame) is True
    alert_button_parent = find_element(
        driver.server_url, driver.session, locator_type, locator_value_alert_parent
    )
    assert get_attribute(driver.server_url, driver.session, alert_button_parent, "any") == "any"
    assert click(driver.server_url, driver.session, alert_button_parent) is True


def test_switch_to_frame_and_click_alert(setup_playground):
    driver = setup_playground
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"

    element_frame = find_element(driver.server_url, driver.session, locator_type, locator_value)
    assert switch_to_frame(driver.server_url, driver.session, element_frame) is True

    alert_button = find_element(
        driver.server_url, driver.session, locator_type, locator_value_alert
    )
    assert get_attribute(driver.server_url, driver.session, alert_button, "any") == "any"
    assert click(driver.server_url, driver.session, alert_button) is True


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
    assert ["display"] == get_property(driver.server_url, driver.session, hidden_button, "style")
    assert "display: none;" == get_attribute(
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
    assert (
        get_property(driver.server_url, driver.session, anchor, property_name="href")
        == "http://any1.com/"
    )

    button = find_element(driver.server_url, driver.session, locator_type, locator_value="//button")
    click(driver.server_url, driver.session, button)

    p = find_element(
        driver.server_url, driver.session, locator_type, locator_value="//p[@id='end']"
    )

    assert get_text(driver.server_url, driver.session, p) == expected
