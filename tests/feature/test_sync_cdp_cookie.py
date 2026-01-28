from pytest import mark

from caqui.cdp.by import By
from caqui.easy.cdp.synchronous.drivers import SyncDriverCDP
from tests.constants import COOKIE


class TestSyncCDPCookies:
    def test_sync_cdp_add_cookie(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        # Need to navigate to a web page. If use 'playgound.html' the error
        # 'Document is cookie-averse' happens
        driver.get(
            "https://example.org/",
        )

        driver.add_cookie(COOKIE)
        cookies_after = driver.get_cookies()
        assert len(cookies_after) > 0

        cookies_before = cookies_after
        cookie = cookies_before[0]
        cookie[By.NAME] = "another"

        driver.add_cookie(cookie)
        cookies_after = driver.get_cookies()
        assert len(cookies_after) > len(cookies_before)

        cookies_after = driver.get_cookies()
        assert len(cookies_after) > len(cookies_before)

    def test_sync_cdp_delete_cookie_asynchronous(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver = setup_sync_cdp_playground
        driver.get(
            "https://example.org/",
        )
        driver.add_cookie(COOKIE)

        cookies = driver.get_cookies()
        name = cookies[0].get(By.NAME)
        driver.delete_cookie(name)
        cookies = driver.get_cookies()
        assert len(cookies) == 0

    def test_sync_cdp_delete_cookies_asynchronous(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        driver.get(
            "https://example.org/",
        )
        driver.add_cookie(COOKIE)
        cookies_before = driver.get_cookies()
        driver.delete_all_cookies()

        cookies_after = driver.get_cookies()
        assert len(cookies_before) != len(cookies_after)

    def test_sync_cdp_get_named_cookie(self, setup_sync_cdp_playground: SyncDriverCDP):
        driver = setup_sync_cdp_playground
        cookie = COOKIE
        expected = "John Doe"
        cookie["name"] = expected
        driver.get(
            "https://example.org/",
        )
        driver.add_cookie(cookie)
        actual = driver.get_cookie(expected)
        assert actual["name"] == expected
