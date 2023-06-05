# necessary import for mokcs
import caqui

from pytest import mark
from caqui import asynchronous
from tests import fake_responses
from unittest.mock import patch


async def mock_post(*args):
    pass


@mark.asyncio
async def test_get_window():
    expected = "845623CAE8115F2B60C9AE8596F13D94"

    async def mock_post(*args):
        return fake_responses.GET_WINDOW

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_property("", "", "", "") == expected


@mark.asyncio
async def test_go_back():
    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.go_back("", "") is True


@mark.asyncio
async def test_get_property():
    expected = "any_value"

    async def mock_post(*args):
        return fake_responses.GET_PROPERTY_VALUE

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_property("", "", "", "") == expected


@mark.asyncio
async def test_get_attribute():
    expected = "any_value"

    async def mock_post(*args):
        return fake_responses.GET_ATTRIBUTE_VALUE

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_attribute("", "", "", "") == expected


@mark.asyncio
async def test_get_url():
    expected = "playground.html"

    async def mock_post(*args):
        return fake_responses.GET_URL

    with patch("caqui.asynchronous.__get", mock_post):
        response = await asynchronous.get_url("", "")
        assert expected in response


@mark.asyncio
async def test_get_timeouts():
    expected = "implicit"

    async def mock_post(*args):
        return fake_responses.GET_TIMEOUTS

    with patch("caqui.asynchronous.__get", mock_post):
        response = await asynchronous.get_timeouts("", "")
        assert expected in response


@mark.asyncio
async def test_get_status():
    async def mock_post(*args):
        return fake_responses.GET_STATUS

    with patch("caqui.asynchronous.__get", mock_post):
        response = await asynchronous.get_status("")
        assert response.get("value").get("ready") is True


@mark.asyncio
async def test_get_title():
    expected = "Sample page"

    async def mock_post(*args):
        return fake_responses.GET_TITLE

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_title("", "") == expected


@mark.asyncio
async def test_get_cookies():
    expected = []

    async def mock_post(*args):
        return fake_responses.GET_COOKIES

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_cookies("", "") == expected


@mark.asyncio
async def test_get_text():
    expected = "any"

    async def mock_post(*args):
        return fake_responses.GET_TEXT

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_text("", "", "") == expected


@mark.asyncio
async def test_close_session():
    with patch("caqui.asynchronous.__delete", mock_post):
        assert await asynchronous.close_session("", "") is True


@mark.asyncio
async def test_go_to_page():
    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.go_to_page("", "", "") is True


@mark.asyncio
async def test_send_keys():
    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.send_keys("", "", "", "") is True


@mark.asyncio
async def test_click():
    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.click("", "", "") is True


@mark.asyncio
async def test_find_elements():
    element = "C230605181E69CB2C4C36B8E83FE1245_element_2"

    async def mock_post(*args):
        return fake_responses.FIND_ELEMENTS

    with patch("caqui.asynchronous.__post", mock_post):
        assert element in await asynchronous.find_elements("", "", "", "")


@mark.asyncio
async def test_find_element():
    element = "0.8851292311864847-1"

    async def mock_post(*args):
        return fake_responses.FIND_ELEMENT

    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.find_element("", "", "", "") == element


@mark.asyncio
async def test_get_session():
    expected = "4358a5b53794586af59678fc1653dc40"

    async def mock_post(*args):
        return fake_responses.GET_SESSION

    with patch("caqui.asynchronous.__post", mock_post):
        assert await asynchronous.get_session("", {}) == expected
