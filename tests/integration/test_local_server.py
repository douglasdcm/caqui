from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

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

# def test_server_uses_edge_webdriver_manager():
#     server = Server(EdgeChromiumDriverManager())
#     server.start()
#     assert server.process is not None
#     server.dispose()
#     assert server.process is None

def test_server_uses_opera_webdriver_manager():
    server = Server(OperaDriverManager())
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
