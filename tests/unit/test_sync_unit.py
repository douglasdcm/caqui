from unittest.mock import patch
from caqui import synchronous
from tests import fake_responses


@patch("requests.request", return_value=fake_responses.GET_RECT)
def test_get_rect(*args):
    expected = {"height": 23, "width": 183, "x": 10, "y": 9652.12}
    assert synchronous.get_rect("", "", "") == expected


@patch("requests.request", return_value=fake_responses.ACTIONS)
def test_actions_scroll_to_element(*args):
    assert synchronous.actions_scroll_to_element("", "", "") == True


@patch("requests.request", return_value=fake_responses.CLICK)
def test_submit(*args):
    assert synchronous.submit("", "", "") == True


@patch("requests.request", return_value=fake_responses.ACTIONS)
def test_actions_click(*args):
    assert synchronous.actions_click("", "", "") == True


@patch("requests.request", return_value=fake_responses.GET_TIMEOUTS)
def test_set_timeouts(*args):
    assert synchronous.set_timeouts("", "", "") == True


@patch("requests.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_children_elements(*args):
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements = synchronous.find_children_elements("", "", "", "", "")

    assert element in elements
    assert len(elements) == 3


@patch("requests.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_child_element(*args):
    expected = "0.8851292311864847-1"

    assert synchronous.find_child_element("", "", "", "", "") == expected


@patch("requests.request", return_value=fake_responses.EXECUTE_SCRIPT)
def test_execute_script(*args):
    expected = "any"

    assert synchronous.execute_script("", "", "", "") == expected


@patch("requests.request", return_value=fake_responses.GET_PAGE_SOURCE)
def test_get_page_source(*args):
    expected = "Sample page"
    assert expected in synchronous.get_page_source("", "")


@patch("requests.request", return_value=fake_responses.GET_ALERT_TEXT)
def test_get_alert_text(*args):
    expected = "any warn"
    assert synchronous.get_alert_text("", "") == expected


@patch("requests.request", return_value=fake_responses.GET_ACTIVE_ELEMENT)
def test_get_active_element(*args):
    expected = "0.8851292311864847-1"
    assert synchronous.get_active_element("", "") == expected


@patch("requests.request", return_value=fake_responses.CLEAR_ELEMENT)
def test_clear_element(*args):
    assert synchronous.clear_element("", "", "") is True


@patch("requests.request", return_value=fake_responses.IS_ELEMENT_ENABLED)
def test_is_element_enabled(*args):
    assert synchronous.is_element_enabled("", "", "") is True


@patch("requests.request", return_value=fake_responses.GET_CSS_COLOR_VALUE)
def test_get_css_value(*args):
    expected = "rgba(0, 0, 0, 1)"
    assert synchronous.get_css_value("", "", "", "") == expected


@patch("requests.request", return_value=fake_responses.IS_ELEMENT_SELECTED)
def test_is_element_selected(*args):
    assert synchronous.is_element_selected("", "", "") is False


@patch("requests.request", return_value=fake_responses.GET_WINDOW_RECTANGLE)
def test_get_window_rectangle(*args):
    expected = "height"

    assert expected in synchronous.get_window_rectangle("", "")


@patch("requests.request", return_value=fake_responses.GET_WINDOW_HANDLES)
def test_get_window_handles(*args):
    expected = "2E55CCE389196328988ED244DAA52A5D"

    assert expected in synchronous.get_window_handles("", "")


@patch("requests.request", return_value=fake_responses.CLOSE_WINDOW)
def test_close_window(*args):
    expected = []

    assert synchronous.close_window("", "") == expected


@patch("requests.request", return_value=fake_responses.GET_WINDOW)
def test_get_window(*args):
    expected = "845623CAE8115F2B60C9AE8596F13D94"

    assert expected in synchronous.get_window("", "")


@patch("requests.request", return_value=fake_responses.GET_URL)
def test_get_url(*args):
    expected = "playground.html"

    assert expected in synchronous.get_url("", "")


@patch("requests.request", return_value=fake_responses.GET_TIMEOUTS)
def test_get_timeouts(*args):
    expected = "implicit"

    assert expected in synchronous.get_timeouts("", "")


@patch("requests.request", return_value=fake_responses.GET_STATUS)
def test_get_status(*args):
    assert synchronous.get_status("").get("value").get("ready") is True


@patch("requests.request", return_value=fake_responses.GET_TITLE)
def test_get_title(*args):
    expected = "Sample page"

    assert synchronous.get_title("", "") == expected


@patch("requests.request", return_value=fake_responses.GET_COOKIES)
def test_get_cookies(*args):
    expected = []

    assert synchronous.get_cookies("", "") == expected


@patch("requests.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_elements(*args):
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements = synchronous.find_elements("", "", "", "")

    assert element in elements
    assert len(elements) == 3


@patch("requests.request", return_value=fake_responses.GET_PROPERTY_VALUE)
def test_get_property(*args):
    expected = "any_value"

    assert synchronous.get_property("", "", "", "") == expected


@patch("requests.request", return_value=fake_responses.GET_ATTRIBUTE_VALUE)
def test_get_attribute(*args):
    expected = "any_value"

    assert synchronous.get_attribute("", "", "", "") == expected


@patch("requests.request", return_value=fake_responses.GO_TO_PAGE)
def test_go_to_page(*args):
    assert synchronous.go_to_page("", "", "") is True


@patch("requests.request", return_value=fake_responses.CLOSE_SESSION)
def test_close_session(*args):
    assert synchronous.close_session("", "") is True


@patch("requests.request", return_value=fake_responses.GET_TEXT)
def test_get_text(*args):
    expected = "any"

    assert synchronous.get_text("", "", "") == expected


@patch("requests.request", return_value=fake_responses.SEND_KEYS)
def test_send_keys(*args):
    assert synchronous.send_keys("", "", "", "") is True


@patch("requests.request", return_value=fake_responses.CLICK)
def test_click(*args):
    assert synchronous.click("", "", "") is True


@patch("requests.request", return_value=fake_responses.GET_SESSION)
def test_get_session(*args):
    expected = "4358a5b53794586af59678fc1653dc40"

    assert synchronous.get_session("", "") == expected


@patch("requests.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_element(*args):
    expected = "0.8851292311864847-1"

    assert synchronous.find_element("", "", "", "") == expected
