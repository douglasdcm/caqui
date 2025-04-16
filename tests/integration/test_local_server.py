from caqui.easy.capabilities import Server
from webdriver_manager.chrome import ChromeDriverManager


def test_server_uses_webdriver_manager():
    server = Server(ChromeDriverManager())
    assert server.process is not None
    server.dispose()
    assert server.process is None


def test_simple_start_and_dispose():
    server = Server()
    assert server.process is not None
    server.dispose()
    assert server.process is None
