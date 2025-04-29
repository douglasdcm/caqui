from caqui.synchronous import (
    find_element,
    click,
    send_keys,
    get_text,
    get_property,
    clear_element,
    get_rect,
    get_css_value,
    get_attribute,
    switch_to_frame,
    switch_to_parent_frame,
    dismiss_alert,
)


def test_switch_to_parent_frame_and_click_alert(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = find_element(server_url, session, locator_type, locator_value)
    assert switch_to_frame(server_url, session, element_frame) is True

    alert_button_frame = find_element(server_url, session, locator_type, locator_value_alert_frame)
    assert click(server_url, session, alert_button_frame) is True
    assert dismiss_alert(server_url, session) is True

    assert switch_to_parent_frame(server_url, session, element_frame) is True
    alert_button_parent = find_element(
        server_url, session, locator_type, locator_value_alert_parent
    )
    assert get_attribute(server_url, session, alert_button_parent, "any") == "any"
    assert click(server_url, session, alert_button_parent) is True


def test_switch_to_frame_and_click_alert(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"

    element_frame = find_element(server_url, session, locator_type, locator_value)
    assert switch_to_frame(server_url, session, element_frame) is True

    alert_button = find_element(server_url, session, locator_type, locator_value_alert)
    assert get_attribute(server_url, session, alert_button, "any") == "any"
    assert click(server_url, session, alert_button) is True


def test_get_data_from_hidden_button(setup_functional_environment):
    server_url, session = setup_functional_environment
    locator_type = "xpath"

    hidden_button = find_element(
        server_url, session, locator_type, locator_value="//*[@id='hidden-button']"
    )

    assert "width" in get_rect(server_url, session, hidden_button)
    assert "visible" == get_css_value(server_url, session, hidden_button, "visibility")
    assert True is get_property(server_url, session, hidden_button, "hidden")
    assert ["display"] == get_property(server_url, session, hidden_button, "style")
    assert "display: none;" == get_attribute(server_url, session, hidden_button, "style")


def test_add_text__click_button_and_get_properties(setup_functional_environment):
    server_url, session = setup_functional_environment
    expected = "end"
    locator_type = "xpath"

    input = find_element(server_url, session, locator_type, locator_value="//input")
    send_keys(server_url, session, input, "any")
    assert get_property(server_url, session, input, property_name="value") == "any"
    clear_element(server_url, session, input)
    assert get_property(server_url, session, input, property_name="value") == ""

    anchor = find_element(server_url, session, locator_type, locator_value="//a")
    assert get_property(server_url, session, anchor, property_name="href") == "http://any1.com/"

    button = find_element(server_url, session, locator_type, locator_value="//button")
    click(server_url, session, button)

    p = find_element(server_url, session, locator_type, locator_value="//p[@id='end']")

    assert get_text(server_url, session, p) == expected
