from pytest import mark

from caqui.easy.server import LocalServer

PORT = 9998


def test_server_uses_firefox_webdriver_manager():
    server = LocalServer()
    server.start_firefox()
    assert server.process is not None
    server.dispose()
    assert server.process is None


def test_server_uses_chrome_webdriver_manager():
    server = LocalServer(PORT)
    server.start_chrome()
    assert server.process is not None
    server.dispose()
    assert server.process is None


# urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='msedgedriver.azureedge.net',
# port=443): Max retries exceeded with url: /LATEST_RELEASE_142_LINUX (Caused by
# NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7a6f35cf6630>:
# Failed to resolve 'msedgedriver.azureedge.net' ([Errno -2] Name or service not known)"))
# similar issue https://github.com/bonigarcia/webdrivermanager/issues/1513
@mark.skip(reason="Webdriver Manager issue")
def test_server_uses_edge_webdriver_manager():
    import time

    server = LocalServer(PORT)
    server.start_edge()
    time.sleep(100)
    assert server.process is not None
    server.dispose()
    assert server.process is None


def test_server_uses_opera_webdriver_manager():
    server = LocalServer(PORT)
    server.start_opera()
    assert server.process is not None
    server.dispose()
    assert server.process is None
