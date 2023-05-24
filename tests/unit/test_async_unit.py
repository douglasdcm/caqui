# from caqui.asynchronous import aiohttp
# from pytest import mark, fixture
# from caqui.asynchronous import (
#     get_session,
#     find_element,
#     click,
#     send_keys,
#     go_to_page,
#     close_session,
#     get_text,
#     get_property_value,
# )
# from unittest.mock import patch
# from tests.doubles.fake_responses import (
#     GET_SESSION,
#     FIND_ELEMENT,
#     CLICK,
#     SEND_KEYS,
#     GO_TO_PAGE,
#     GET_TEXT,
# )


# class MockRequest:
#     def __init__(self, return_value) -> None:
#         self.__return_value = return_value

#     def release(*args):
#         pass

#     async def session(self, *args):
#         return self.__return_value

#     def json(self, *args):
#         return self.session(*args)


# def request_mock(*args):
#     return MockRequest(*args)


# @fixture
# def __setup():
#     driver_url = "http://127.0.0.1:9999"
#     session = "4358a5b53794586af59678fc1653dc40"
#     element = "0.8851292311864847-1"

#     return driver_url, session, element


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(GET_TEXT))
# async def test_get_property_value(mock, __setup):
#     driver_url, session, element = __setup
#     text = "any"

#     assert await get_property_value(driver_url, session, element) == text


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(GET_TEXT))
# async def test_get_text(mock, __setup):
#     driver_url, session, element = __setup
#     text = "any"

#     assert await get_text(driver_url, session, element) == text


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(GET_SESSION))
# async def test_close_session(mock, __setup):
#     driver_url, session, _ = __setup

#     assert await close_session(driver_url, session) == session


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(GO_TO_PAGE))
# async def test_go_to_page(mock, __setup):
#     driver_url, session, _ = __setup
#     url = "http://any.com"

#     assert await go_to_page(driver_url, session, url) == session


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(SEND_KEYS))
# async def test_send_keys(mock, __setup):
#     driver_url, session, element = __setup
#     text = "any"

#     assert await send_keys(driver_url, session, element, text) == session


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(CLICK))
# async def test_click(mock, __setup):
#     driver_url, session, element = __setup

#     assert await click(driver_url, session, element) == session


# @mark.asyncio
# @patch("aiohttp.ClientSession._request", return_value=request_mock(FIND_ELEMENT))
# async def test_find_element(mock, __setup):
#     driver_url, session, element = __setup
#     locator_type = "xpath"
#     locator_value = "//input"

#     assert (
#         await find_element(driver_url, session, locator_type, locator_value) == element
#     )


# from unittest.mock import MagicMock
# from caqui.asynchronous import aiohttp


# @mark.asyncio
# # @patch("caqui.asynchronous.aiohttp.client", autospec=True)
# # @patch("caqui.asynchronous.aiohttp.ClientSession.post", autospec=True)
# # @patch("caqui.asynchronous.aiohttp.client", return_value=MockRequest)
# # @patch(
# #     "caqui.asynchronous.aiohttp.ClientSession._request",
# #     return_value=request_mock(GET_SESSION),
# # )
# async def test_get_session(*args):
#     driver_url = "http://any:9999"
#     capabilities = {
#         "desiredCapabilities": {
#             "browserName": "firefox",
#             "marionette": True,
#             "acceptInsecureCerts": True,
#         }
#     }
#     expected = "4358a5b53794586af59678fc1653dc40"

#     from caqui.asynchronous import aiohttp

#     class Inner:
#         async def json():
#             pass

#     class AEnterExit:
#         def __await__(*args):
#             yield Inner()

#     class MockPost:
#         def __init__(*args, **kwargs):
#             pass

#         def __aexit__(*args, **kwargs):
#             return AEnterExit()

#         def __aenter__(*args, **kwargs):
#             return AEnterExit()

#     aiohttp.client = MagicMock()
#     aiohttp.ClientSession.post = MockPost

#     assert await get_session(driver_url, capabilities) == expected
