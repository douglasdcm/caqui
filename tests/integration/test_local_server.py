from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from caqui.easy.server import Server


def test_server_uses_firefor_webdriver_manager():
    server = Server(GeckoDriverManager())
    server.start()
    assert server.process is not None
    server.dispose()
    assert server.process is None


def test_server_uses_chrome_webdriver_manager():
    server = Server(ChromeDriverManager())
    server.start()
    assert server.process is not None
    server.dispose()
    assert server.process is None


def test_simple_start_and_dispose():
    server = Server()
    server.start()
    assert server.process is not None
    server.dispose()
    assert server.process is None
