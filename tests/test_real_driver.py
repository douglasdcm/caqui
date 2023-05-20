import json
from caqui.driver.sdk import (
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property_value,
)
from pytest import fixture


@fixture
def __setup():
    driver_url = "http://127.0.0.1:9999"
    capabilities = json.dumps(
        {
            "desiredCapabilities": {
                "browserName": "firefox",
                "marionette": True,
                "acceptInsecureCerts": True,
            }
        }
    )
    session = get_session(driver_url, capabilities)
    go_to_page(
        driver_url,
        session,
        "file:///home/douglas/repo/caqui/caqui/tests/playground.html",
    )
    yield driver_url, session
    close_session(driver_url, session)


def test_get_property_value(__setup):
    driver_url, session = __setup
    text = "any_value"
    locator_type = "xpath"
    locator_value = "//input"

    element = find_element(driver_url, session, locator_type, locator_value)
    send_keys(driver_url, session, element, text)

    assert get_property_value(driver_url, session, element) == text


def test_get_text(__setup):
    driver_url, session = __setup
    expected = "end"
    locator_type = "xpath"
    locator_value = "//p[@id='end']"  # <p>end</p>

    element = find_element(driver_url, session, locator_type, locator_value)

    assert get_text(driver_url, session, element) == expected


def test_send_keys(__setup):
    driver_url, session = __setup
    text = "any"
    locator_type = "xpath"
    locator_value = "//input"
    expected = session

    element = find_element(driver_url, session, locator_type, locator_value)

    assert send_keys(driver_url, session, element, text) == expected


def test_click(__setup):
    driver_url, session = __setup
    locator_type = "xpath"
    locator_value = "//button"
    expected = session

    element = find_element(driver_url, session, locator_type, locator_value)

    assert click(driver_url, session, element) == expected
