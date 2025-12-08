import aiohttp
from pytest import mark, raises

from caqui import synchronous
from caqui.by import By
from caqui.easy.drivers import AsyncDriver
from caqui.exceptions import WebDriverError
from tests.constants import COOKIE, OTHER_URL, PAGE_URL


@mark.asyncio
async def test_add_cookie(setup_playground: AsyncDriver):
    driver = setup_playground
    # Need to navigate to a web page. If use 'playgound.html' the error
    # 'Document is cookie-averse' happens
    await driver.get(
        "https://example.org/",
    )
    cookie = COOKIE
    assert await driver.add_cookie(cookie) is True
    cookies_after = await driver.get_cookies()
    assert len(cookies_after) > 0

    cookies_before = cookies_after
    cookie = cookies_before[0]
    cookie[By.NAME] = "another"

    assert await driver.add_cookie(cookie) is True
    cookies_after = await driver.get_cookies()
    assert len(cookies_after) > len(cookies_before)

    cookies_after = await driver.get_cookies()
    assert len(cookies_after) > len(cookies_before)


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookie_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground
    cookies = await driver.get_cookies()
    name = cookies[0].get(By.NAME)
    zero = 0

    assert await driver.delete_cookie(name) is True
    cookies = await driver.get_cookies()
    assert len(cookies) == zero

    cookies = await driver.get_cookies()
    assert len(cookies) == zero


@mark.skip(reason="works just in firefox")
@mark.asyncio
async def test_delete_cookies_asynchronous(setup_playground: AsyncDriver):
    driver = setup_playground

    cookies_before = await driver.get_cookies()

    response = await driver.delete_all_cookies()
    assert response is True

    cookies_after = await driver.get_cookies()
    assert len(cookies_before) != len(cookies_after)


@mark.skip(reason="works just with Firefox")
@mark.asyncio
async def test_get_named_cookie(setup_playground: AsyncDriver):
    driver = setup_playground
    name = "username"  # cookie created on page load
    expected = "John Doe"

    assert await driver.get_named_cookie(name).get("value") == expected
    response = await driver.get_named_cookie(name)
    assert response == expected
