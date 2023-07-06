# necessary import for mokcs
import caqui

from pytest import mark
from caqui import asynchronous
from tests import fake_responses
from unittest.mock import patch


async def mock_request(*args):
    pass


@mark.asyncio
async def test_get_rect():
    expected = {"height": 23, "width": 183, "x": 10, "y": 9652.12}

    async def mock_request(*args):
        return fake_responses.GET_RECT

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_rect("", "", "") == expected


@mark.asyncio
async def test_actions_scroll_to_element():
    async def mock_request(*args):
        return fake_responses.ACTIONS

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.actions_scroll_to_element("", "", "") == True


@mark.asyncio
async def test_submit():
    async def mock_request(*args):
        return fake_responses.CLICK

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.submit("", "", "") == True


@mark.asyncio
async def test_actions_click():
    async def mock_request(*args):
        return fake_responses.ACTIONS

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.actions_click("", "", "") == True


@mark.asyncio
async def test_set_timeouts():
    async def mock_request(*args):
        return fake_responses.GET_TIMEOUTS

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.set_timeouts("", "", "") == True


@mark.asyncio
async def test_find_children_elements():
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    async def mock_request(*args):
        return fake_responses.FIND_ELEMENTS

    with patch("caqui.asynchronous.__post", mock_request):
        assert element in await asynchronous.find_children_elements("", "", "", "", "")


@mark.asyncio
async def test_find_child_element():
    element = "0.8851292311864847-1"

    async def mock_request(*args):
        return fake_responses.FIND_ELEMENT

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.find_child_element("", "", "", "", "") == element


@mark.asyncio
async def test_execute_script():
    expected = "any"

    async def mock_request(*args):
        return fake_responses.EXECUTE_SCRIPT

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.execute_script("", "", "", "") == expected


@mark.asyncio
async def test_get_page_source():
    expected = "Sample page"

    async def mock_request(*args):
        return fake_responses.GET_PAGE_SOURCE

    with patch("caqui.asynchronous.__get", mock_request):
        assert expected in await asynchronous.get_page_source("", "")


@mark.asyncio
async def test_get_alert_text():
    expected = "any warn"

    async def mock_request(*args):
        return fake_responses.GET_ALERT_TEXT

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_alert_text("", "") == expected


@mark.asyncio
async def test_get_active_element():
    expected = "0.8851292311864847-1"

    async def mock_request(*args):
        return fake_responses.GET_ACTIVE_ELEMENT

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_active_element("", "") == expected


@mark.asyncio
async def test_clear_element():
    async def mock_request(*args):
        return fake_responses.CLEAR_ELEMENT

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.clear_element("", "", "") is True


@mark.asyncio
async def test_is_element_enabled():
    async def mock_request(*args):
        return fake_responses.IS_ELEMENT_ENABLED

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.is_element_enabled("", "", "") is True


@mark.asyncio
async def test_get_css_value():
    expected = "rgba(0, 0, 0, 1)"

    async def mock_request(*args):
        return fake_responses.GET_CSS_COLOR_VALUE

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_css_value("", "", "", "") == expected


@mark.asyncio
async def test_is_element_selected():
    async def mock_request(*args):
        return fake_responses.IS_ELEMENT_SELECTED

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.is_element_selected("", "", "") is False


@mark.asyncio
async def test_get_window_rectangle():
    expected = "height"

    async def mock_request(*args):
        return fake_responses.GET_WINDOW_RECTANGLE

    with patch("caqui.asynchronous.__get", mock_request):
        assert expected in await asynchronous.get_window_rectangle("", "")


@mark.asyncio
async def test_get_window_handles():
    expected = ["2E55CCE389196328988ED244DAA52A5D"]

    async def mock_request(*args):
        return fake_responses.GET_WINDOW_HANDLES

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_window_handles("", "") == expected


@mark.asyncio
async def test_close_window():
    expected = []

    async def mock_request(*args):
        return fake_responses.CLOSE_WINDOW

    with patch("caqui.asynchronous.__delete", mock_request):
        assert await asynchronous.close_window("", "") == expected


@mark.asyncio
async def test_get_window():
    expected = "845623CAE8115F2B60C9AE8596F13D94"

    async def mock_request(*args):
        return fake_responses.GET_WINDOW

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_window("", "") == expected


@mark.asyncio
async def test_go_back():
    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.go_back("", "") is True


@mark.asyncio
async def test_get_property():
    expected = "any_value"

    async def mock_request(*args):
        return fake_responses.GET_PROPERTY_VALUE

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_property("", "", "", "") == expected


@mark.asyncio
async def test_get_attribute():
    expected = "any_value"

    async def mock_request(*args):
        return fake_responses.GET_ATTRIBUTE_VALUE

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_attribute("", "", "", "") == expected


@mark.asyncio
async def test_get_url():
    expected = "playground.html"

    async def mock_request(*args):
        return fake_responses.GET_URL

    with patch("caqui.asynchronous.__get", mock_request):
        response = await asynchronous.get_url("", "")
        assert expected in response


@mark.asyncio
async def test_get_timeouts():
    expected = "implicit"

    async def mock_request(*args):
        return fake_responses.GET_TIMEOUTS

    with patch("caqui.asynchronous.__get", mock_request):
        response = await asynchronous.get_timeouts("", "")
        assert expected in response


@mark.asyncio
async def test_get_status():
    async def mock_request(*args):
        return fake_responses.GET_STATUS

    with patch("caqui.asynchronous.__get", mock_request):
        response = await asynchronous.get_status("")
        assert response.get("value").get("ready") is True


@mark.asyncio
async def test_get_title():
    expected = "Sample page"

    async def mock_request(*args):
        return fake_responses.GET_TITLE

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_title("", "") == expected


@mark.asyncio
async def test_get_cookies():
    expected = []

    async def mock_request(*args):
        return fake_responses.GET_COOKIES

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_cookies("", "") == expected


@mark.asyncio
async def test_get_text():
    expected = "any"

    async def mock_request(*args):
        return fake_responses.GET_TEXT

    with patch("caqui.asynchronous.__get", mock_request):
        assert await asynchronous.get_text("", "", "") == expected


@mark.asyncio
async def test_close_session():
    with patch("caqui.asynchronous.__delete", mock_request):
        assert await asynchronous.close_session("", "") is True


@mark.asyncio
async def test_go_to_page():
    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.go_to_page("", "", "") is True


@mark.asyncio
async def test_send_keys():
    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.send_keys("", "", "", "") is True


@mark.asyncio
async def test_click():
    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.click("", "", "") is True


@mark.asyncio
async def test_find_elements():
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    async def mock_request(*args):
        return fake_responses.FIND_ELEMENTS

    with patch("caqui.asynchronous.__post", mock_request):
        assert element in await asynchronous.find_elements("", "", "", "")


@mark.asyncio
async def test_find_element():
    element = "0.8851292311864847-1"

    async def mock_request(*args):
        return fake_responses.FIND_ELEMENT

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.find_element("", "", "", "") == element


@mark.asyncio
async def test_get_session():
    expected = "4358a5b53794586af59678fc1653dc40"

    async def mock_request(*args):
        return fake_responses.GET_SESSION

    with patch("caqui.asynchronous.__post", mock_request):
        assert await asynchronous.get_session("", {}) == expected
