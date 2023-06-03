# necessary import for mokcs
import caqui

from pytest import mark
from caqui import asynchronous
from tests import fake_responses


async def mock_post(*args):
    pass


@mark.asyncio
async def test_get_property():
    expected = "any_value"

    async def mock_post(*args):
        return fake_responses.GET_PROPERTY_VALUE

    with patch("caqui.asynchronous.__get", mock_post):
        assert await asynchronous.get_property("", "", "", "") == expected


from unittest.mock import patch


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
