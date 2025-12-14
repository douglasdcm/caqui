from unittest.mock import patch

from caqui import synchronous
from tests import fake_responses


@patch("caqui.synchronous.request", return_value=fake_responses.GET_RECT)
def test_get_rect(*args: tuple) -> None:
    expected: dict = {"height": 23, "width": 183, "x": 10, "y": 9652.12}
    assert synchronous.get_rect("", "", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.ACTIONS)
def test_actions_scroll_to_element(*args: tuple) -> None:
    assert synchronous.actions_scroll_to_element("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.CLICK)
def test_submit(*args: tuple) -> None:
    assert synchronous.submit("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.ACTIONS)
def test_actions_click(*args: tuple) -> None:
    assert synchronous.actions_click("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.GET_TIMEOUTS)
def test_set_timeouts(*args: tuple) -> None:
    assert synchronous.set_timeouts("", "", 0) is True


@patch("caqui.synchronous.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_children_elements(*args: tuple) -> None:
    element: str = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements: list = synchronous.find_children_elements("", "", "", "xpath", "")

    assert element in elements
    assert len(elements) == 3


@patch("caqui.synchronous.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_child_element(*args: tuple) -> None:
    expected: str = "0.8851292311864847-1"

    assert synchronous.find_child_element("", "", "", "xpath", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.EXECUTE_SCRIPT)
def test_execute_script(*args: tuple) -> None:
    expected: str = "any"

    assert synchronous.execute_script("", "", "", [""]) == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GET_PAGE_SOURCE)
def test_get_page_source(*args: tuple) -> None:
    expected: str = "Sample page"
    assert expected in synchronous.get_page_source("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.GET_ALERT_TEXT)
def test_get_alert_text(*args: tuple) -> None:
    expected: str = "any warn"
    assert synchronous.get_alert_text("", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GET_ACTIVE_ELEMENT)
def test_get_active_element(*args: tuple) -> None:
    expected: str = "0.8851292311864847-1"
    assert synchronous.get_active_element("", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.CLEAR_ELEMENT)
def test_clear_element(*args: tuple) -> None:
    assert synchronous.clear_element("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.IS_ELEMENT_ENABLED)
def test_is_element_enabled(*args: tuple) -> None:
    assert synchronous.is_element_enabled("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.GET_CSS_COLOR_VALUE)
def test_get_css_value(*args: tuple) -> None:
    expected: str = "0, 0, 0"
    assert expected in synchronous.get_css_value("", "", "", "")


@patch("caqui.synchronous.request", return_value=fake_responses.IS_ELEMENT_SELECTED)
def test_is_element_selected(*args: tuple) -> None:
    assert synchronous.is_element_selected("", "", "") is False


@patch("caqui.synchronous.request", return_value=fake_responses.GET_WINDOW_RECTANGLE)
def test_get_window_rectangle(*args: tuple) -> None:
    expected: str = "height"

    assert expected in synchronous.get_window_rectangle("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.GET_WINDOW_HANDLES)
def test_get_window_handles(*args: tuple) -> None:
    expected: str = "2E55CCE389196328988ED244DAA52A5D"

    assert expected in synchronous.get_window_handles("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.CLOSE_WINDOW)
def test_close_window(*args: tuple) -> None:
    expected: list = []

    assert synchronous.close_window("", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GET_WINDOW)
def test_get_window(*args: tuple) -> None:
    expected: str = "845623CAE8115F2B60C9AE8596F13D94"

    assert expected in synchronous.get_window("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.GET_URL)
def test_get_url(*args: tuple) -> None:
    expected: str = "playground.html"

    assert expected in synchronous.get_url("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.GET_TIMEOUTS)
def test_get_timeouts(*args: tuple) -> None:
    expected: str = "implicit"

    assert expected in synchronous.get_timeouts("", "")


@patch("caqui.synchronous.request", return_value=fake_responses.GET_STATUS)
def test_get_status(*args: tuple) -> None:
    assert synchronous.get_status("").get("value", {}).get("ready", False) is True


@patch("caqui.synchronous.request", return_value=fake_responses.GET_TITLE)
def test_get_title(*args: tuple) -> None:
    expected: str = "Sample page"

    assert synchronous.get_title("", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GET_COOKIES)
def test_get_cookies(*args: tuple) -> None:
    expected: list = []

    assert synchronous.get_cookies("", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.FIND_ELEMENTS)
def test_find_elements(*args: tuple) -> None:
    element: str = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    elements: list = synchronous.find_elements("", "", "xpath", "")

    assert element in elements
    assert len(elements) == 3


@patch("caqui.synchronous.request", return_value=fake_responses.GET_PROPERTY_VALUE)
def test_get_property(*args: tuple) -> None:
    expected: str = "any_value"

    assert synchronous.get_property("", "", "", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GET_ATTRIBUTE_VALUE)
def test_get_attribute(*args: tuple) -> None:
    expected: str = "any_value"

    assert synchronous.get_attribute("", "", "", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.GO_TO_PAGE)
def test_go_to_page(*args: tuple) -> None:
    assert synchronous.go_to_page("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.CLOSE_SESSION)
def test_close_session(*args: tuple) -> None:
    assert synchronous.close_session("", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.GET_TEXT)
def test_get_text(*args: tuple) -> None:
    expected: str = "any"

    assert synchronous.get_text("", "", "") == expected


@patch("caqui.synchronous.request", return_value=fake_responses.SEND_KEYS)
def test_send_keys(*args: tuple) -> None:
    assert synchronous.send_keys("", "", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.CLICK)
def test_click(*args: tuple) -> None:
    assert synchronous.click("", "", "") is True


@patch("caqui.synchronous.request", return_value=fake_responses.GET_SESSION)
def test_get_session(*args: tuple) -> None:
    expected: str = "4358a5b53794586af59678fc1653dc40"

    assert synchronous.get_session(server_url="", capabilities={}) == expected


@patch("caqui.synchronous.request", return_value=fake_responses.FIND_ELEMENT)
def test_find_element(*args: tuple) -> None:
    expected: str = "0.8851292311864847-1"

    assert synchronous.find_element("", "", "xpath", "") == expected
