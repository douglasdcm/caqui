from unittest.mock import patch
from caqui.synchronous import (
    find_element,
    get_session,
    click,
    send_keys,
    get_text,
    close_session,
    go_to_page,
    get_property,
    find_elements,
)
from tests.fake_responses import (
    FIND_ELEMENT,
    GET_SESSION,
    CLICK,
    GET_TEXT,
    CLOSE_SESSION,
    GO_TO_PAGE,
    GET_PROPERTY_VALUE,
    SEND_KEYS,
    FIND_ELEMENTS,
)


def __setup():
    driver_url = "http://any:9999"
    session = "4358a5b53794586af59678fc1653dc40"
    element = "0.8851292311864847-1"
    return driver_url, session, element


@patch("requests.request", return_value=FIND_ELEMENTS)
def test_find_elements(*args):
    driver_url, session, _ = __setup()
    locator_type = "xpath"
    locator_value = "//input"
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements = find_elements(driver_url, session, locator_type, locator_value)

    assert element in elements
    assert len(elements) == 3


@patch("requests.request", return_value=GET_PROPERTY_VALUE)
def test_get_property(*args):
    driver_url, session, _ = __setup()
    element = "any"
    property = "value"
    expected = "any_value"

    assert get_property(driver_url, session, element, property) == expected


@patch("requests.request", return_value=GO_TO_PAGE)
def test_go_to_page(*args):
    driver_url, session, _ = __setup()
    url = "http://any.com"

    assert go_to_page(driver_url, session, url) == session


@patch("requests.request", return_value=CLOSE_SESSION)
def test_close_session(*args):
    driver_url, session, _ = __setup()

    assert close_session(driver_url, session) == session


@patch("requests.request", return_value=GET_TEXT)
def test_get_text(*args):
    driver_url, session, element = __setup()
    expected = "any"

    assert get_text(driver_url, session, element) == expected


@patch("requests.request", return_value=SEND_KEYS)
def test_send_keys(*args):
    driver_url, session, element = __setup()
    text = "any"

    assert send_keys(driver_url, session, element, text) == session


@patch("requests.request", return_value=CLICK)
def test_click(*args):
    driver_url, session, element = __setup()

    assert click(driver_url, session, element) == session


@patch("requests.request", return_value=GET_SESSION)
def test_get_session(*args):
    driver_url = "http://any:9999"
    payload = {
        "desiredCapabilities": {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
        }
    }
    expected = "4358a5b53794586af59678fc1653dc40"

    assert get_session(driver_url, payload) == expected


@patch("requests.request", return_value=FIND_ELEMENT)
def test_find_element(*args):
    driver_url, session, _ = __setup()
    locator_type = "xpath"
    locator_value = "//input"
    expected = "0.8851292311864847-1"

    assert find_element(driver_url, session, locator_type, locator_value) == expected
