from unittest.mock import patch
from caqui import synchronous
from tests import fake_responses


def __setup():
    driver_url = "http://any:9999"
    session = "4358a5b53794586af59678fc1653dc40"
    element = "0.8851292311864847-1"
    return driver_url, session, element


@patch("requests.request", return_value=fake_responses.GET_STATUS)
def test_get_status(*args):
    driver_url, _, _ = __setup()

    assert synchronous.get_status(driver_url).get("value").get("ready") is True


@patch("requests.request", return_value=fake_responses.GET_TITLE)
def test_get_title(*args):
    driver_url, session, _ = __setup()
    expected = "Sample page"

    assert synchronous.get_title(driver_url, session) == expected


@patch("requests.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_elements(*args):
    driver_url, session, _ = __setup()
    locator_type = "xpath"
    locator_value = "//input"
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements = synchronous.find_elements(
        driver_url, session, locator_type, locator_value
    )

    assert element in elements
    assert len(elements) == 3


@patch("requests.request", return_value=fake_responses.GET_PROPERTY_VALUE)
def test_get_property(*args):
    driver_url, session, _ = __setup()
    element = "any"
    property = "value"
    expected = "any_value"

    assert synchronous.get_property(driver_url, session, element, property) == expected


@patch("requests.request", return_value=fake_responses.GO_TO_PAGE)
def test_go_to_page(*args):
    driver_url, session, _ = __setup()
    url = "http://any.com"

    assert synchronous.go_to_page(driver_url, session, url) is True


@patch("requests.request", return_value=fake_responses.CLOSE_SESSION)
def test_close_session(*args):
    driver_url, session, _ = __setup()

    assert synchronous.close_session(driver_url, session) is True


@patch("requests.request", return_value=fake_responses.GET_TEXT)
def test_get_text(*args):
    driver_url, session, element = __setup()
    expected = "any"

    assert synchronous.get_text(driver_url, session, element) == expected


@patch("requests.request", return_value=fake_responses.SEND_KEYS)
def test_send_keys(*args):
    driver_url, session, element = __setup()
    text = "any"

    assert synchronous.send_keys(driver_url, session, element, text) is True


@patch("requests.request", return_value=fake_responses.CLICK)
def test_click(*args):
    driver_url, session, element = __setup()

    assert synchronous.click(driver_url, session, element) is True


@patch("requests.request", return_value=fake_responses.GET_SESSION)
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

    assert synchronous.get_session(driver_url, payload) == expected


@patch("requests.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_element(*args):
    driver_url, session, _ = __setup()
    locator_type = "xpath"
    locator_value = "//input"
    expected = "0.8851292311864847-1"

    assert (
        synchronous.find_element(driver_url, session, locator_type, locator_value)
        == expected
    )
