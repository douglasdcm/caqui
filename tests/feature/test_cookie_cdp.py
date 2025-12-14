from pytest import mark

from caqui.by import By
from caqui.easy.cdp.drivers import AsyncDriver
from tests.constants import COOKIE


class TestCDPCookies:
    @mark.asyncio
    async def test_cdp_add_cookie(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        # Need to navigate to a web page. If use 'playgound.html' the error
        # 'Document is cookie-averse' happens
        await driver.get(
            "https://example.org/",
        )

        await driver.add_cookie(COOKIE)
        cookies_after = await driver.get_cookies()
        assert len(cookies_after) > 0

        cookies_before = cookies_after
        cookie = cookies_before[0]
        cookie[By.NAME] = "another"

        await driver.add_cookie(cookie)
        cookies_after = await driver.get_cookies()
        assert len(cookies_after) > len(cookies_before)

        cookies_after = await driver.get_cookies()
        assert len(cookies_after) > len(cookies_before)

    @mark.asyncio
    async def test_cdp_delete_cookie_asynchronous(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        driver = setup_cdp_playground
        await driver.get(
            "https://example.org/",
        )
        await driver.add_cookie(COOKIE)

        cookies = await driver.get_cookies()
        name = cookies[0].get(By.NAME)
        await driver.delete_cookie(name)
        cookies = await driver.get_cookies()
        assert len(cookies) == 0

    @mark.asyncio
    async def test_cdp_delete_cookies_asynchronous(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        await driver.get(
            "https://example.org/",
        )
        await driver.add_cookie(COOKIE)
        cookies_before = await driver.get_cookies()
        await driver.delete_all_cookies()

        cookies_after = await driver.get_cookies()
        assert len(cookies_before) != len(cookies_after)

    @mark.asyncio
    async def test_cdp_get_named_cookie(self, setup_cdp_playground: AsyncDriver):
        driver = setup_cdp_playground
        cookie = COOKIE
        expected = "John Doe"
        cookie["name"] = expected
        await driver.get(
            "https://example.org/",
        )
        await driver.add_cookie(cookie)
        actual = await driver.get_cookie(expected)
        assert actual["name"] == expected
