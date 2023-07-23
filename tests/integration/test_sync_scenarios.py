from caqui.synchronous import (
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property,
    clear_element,
    get_rect,
    get_css_value,
    get_attribute,
    switch_to_frame,
    switch_to_parent_frame,
    dismiss_alert,
)
from tests.constants import PAGE_URL
from pytest import fixture


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "chrome",
            "marionette": True,
            "acceptInsecureCerts": True,
            "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
        }
    }
    session = get_session(driver_url, capabilities)
    go_to_page(
        driver_url,
        session,
        PAGE_URL,
    )
    yield driver_url, session
    close_session(driver_url, session)


def test_switch_to_parent_frame_and_click_alert(__setup):
    driver_url, session = __setup
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = find_element(driver_url, session, locator_type, locator_value)
    assert switch_to_frame(driver_url, session, element_frame) is True

    alert_button_frame = find_element(
        driver_url, session, locator_type, locator_value_alert_frame
    )
    assert click(driver_url, session, alert_button_frame) is True
    assert dismiss_alert(driver_url, session) is True

    assert switch_to_parent_frame(driver_url, session, element_frame) is True
    alert_button_parent = find_element(
        driver_url, session, locator_type, locator_value_alert_parent
    )
    assert get_attribute(driver_url, session, alert_button_parent, "any") == "any"
    assert click(driver_url, session, alert_button_parent) is True


def test_switch_to_frame_and_click_alert(__setup):
    driver_url, session = __setup
    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert = "alert-button-iframe"

    element_frame = find_element(driver_url, session, locator_type, locator_value)
    assert switch_to_frame(driver_url, session, element_frame) is True

    alert_button = find_element(driver_url, session, locator_type, locator_value_alert)
    assert get_attribute(driver_url, session, alert_button, "any") == "any"
    assert click(driver_url, session, alert_button) is True


def test_get_data_from_hidden_button(__setup):
    driver_url, session = __setup
    locator_type = "xpath"

    hidden_button = find_element(
        driver_url, session, locator_type, locator_value="//*[@id='hidden-button']"
    )

    assert "width" in get_rect(driver_url, session, hidden_button)
    assert "visible" == get_css_value(driver_url, session, hidden_button, "visibility")
    assert True == get_property(driver_url, session, hidden_button, "hidden")
    assert ["display"] == get_property(driver_url, session, hidden_button, "style")
    assert "display: none;" == get_attribute(
        driver_url, session, hidden_button, "style"
    )


def test_add_text__click_button_and_get_properties(__setup):
    driver_url, session = __setup
    expected = "end"
    locator_type = "xpath"

    input = find_element(driver_url, session, locator_type, locator_value="//input")
    send_keys(driver_url, session, input, "any")
    assert get_property(driver_url, session, input, property_name="value") == "any"
    clear_element(driver_url, session, input)
    assert get_property(driver_url, session, input, property_name="value") == ""

    anchor = find_element(driver_url, session, locator_type, locator_value="//a")
    assert (
        get_property(driver_url, session, anchor, property_name="href")
        == "http://any1.com/"
    )

    button = find_element(driver_url, session, locator_type, locator_value="//button")
    click(driver_url, session, button)

    p = find_element(driver_url, session, locator_type, locator_value="//p[@id='end']")

    assert get_text(driver_url, session, p) == expected
