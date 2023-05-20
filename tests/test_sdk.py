import json
from unittest.mock import MagicMock
from caqui.driver.sdk import (
    requests,
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property_value,
)
from tests.doubles.fake_responses import (
    FIND_ELEMENT,
    GET_SESSION,
    CLICK,
    GET_TEXT,
    CLOSE_SESSION,
    GO_TO_PAGE,
    GET_PROPERTY_VALUE,
)


def __setup():
    driver_url = "http://127.0.0.1:9999"
    session = "4358a5b53794586af59678fc1653dc40"
    element = "0.8851292311864847-1"
    return driver_url, session, element


def test_get_property_value():
    driver_url, session, _ = __setup()
    element = "any"
    expected = "any_value"
    requests.request = MagicMock(return_value=GET_PROPERTY_VALUE)

    assert get_property_value(driver_url, session, element) == expected


def test_go_to_page():
    driver_url, session, _ = __setup()
    url = "http://any.com"
    requests.request = MagicMock(return_value=GO_TO_PAGE)

    assert go_to_page(driver_url, session, url) == session


def test_close_session():
    driver_url, session, _ = __setup()
    requests.request = MagicMock(return_value=CLOSE_SESSION)

    assert close_session(driver_url, session) == session


def test_get_text():
    driver_url, session, element = __setup()
    expected = "any"
    requests.request = MagicMock(return_value=GET_TEXT)

    assert get_text(driver_url, session, element) == expected


def test_send_keys():
    driver_url, session, element = __setup()
    text = "any"
    requests.request = MagicMock(return_value=CLICK)

    assert send_keys(driver_url, session, element, text) == session


def test_click():
    driver_url, session, element = __setup()
    requests.request = MagicMock(return_value=CLICK)

    assert click(driver_url, session, element) == session


def test_get_session():
    driver_url = "http://127.0.0.1:9999"
    payload = json.dumps(
        {
            "desiredCapabilities": {
                "browserName": "firefox",
                "marionette": True,
                "acceptInsecureCerts": True,
            }
        }
    )
    expected = "4358a5b53794586af59678fc1653dc40"
    requests.request = MagicMock(return_value=GET_SESSION)

    assert get_session(driver_url, payload) == expected


def test_find_element():
    driver_url, session, _ = __setup()
    locator_type = "xpath"
    locator_value = "//input"
    expected = "0.8851292311864847-1"
    requests.request = MagicMock(return_value=FIND_ELEMENT)

    assert find_element(driver_url, session, locator_type, locator_value) == expected
