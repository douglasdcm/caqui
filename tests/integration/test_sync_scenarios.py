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
    assert get_property(driver_url, session, input, property="value") == "any"
    clear_element(driver_url, session, input)
    assert get_property(driver_url, session, input, property="value") == ""

    anchor = find_element(driver_url, session, locator_type, locator_value="//a")
    assert (
        get_property(driver_url, session, anchor, property="href") == "http://any1.com/"
    )

    button = find_element(driver_url, session, locator_type, locator_value="//button")
    click(driver_url, session, button)

    p = find_element(driver_url, session, locator_type, locator_value="//p[@id='end']")
    get_text(driver_url, session, p)

    assert get_text(driver_url, session, p) == expected
