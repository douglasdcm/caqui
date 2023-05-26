import json
from caqui.synchronous import (
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property,
)
from tests.constants import PAGE_URL
from pytest import fixture


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
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


def test_add_text__click_button_and_get_properties(__setup):
    driver_url, session = __setup
    expected = "end"
    locator_type = "xpath"

    input = find_element(driver_url, session, locator_type, locator_value="//input")
    send_keys(driver_url, session, input, "any")
    assert get_property(driver_url, session, input, property="value") == "any"

    anchor = find_element(driver_url, session, locator_type, locator_value="//a")
    assert (
        get_property(driver_url, session, anchor, property="href") == "http://any1.com/"
    )

    button = find_element(driver_url, session, locator_type, locator_value="//button")
    click(driver_url, session, button)

    p = find_element(driver_url, session, locator_type, locator_value="//p[@id='end']")
    get_text(driver_url, session, p)

    assert get_text(driver_url, session, p) == expected
