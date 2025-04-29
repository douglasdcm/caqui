# Caqui

[![PyPI Downloads](https://static.pepy.tech/badge/caqui)](https://pepy.tech/projects/caqui)

**Caqui** executes commands against Drivers synchronously and asynchronously. The intention is that the user does not worry about which Driver they're using. It can be **Web**Drivers like [Selenium](https://www.selenium.dev/), **Mobile**Drivers like [Appium](http://appium.io/docs/en/2.0/), or **Desktop**Drivers like [Winium](https://github.com/2gis/Winium.Desktop). It can also be used in remote calls. The user can start the Driver as a server in any host and provide the URL to **Caqui** clients.

# Tested WebDrivers

| WebDriver               | Version       | Remote* | Comment |
| ----------------------- | ------------- | ------- |-------- |
| Appium                  | 2.0.0+        | Y       | Accepts remote calls by default. Tested with Appium in Docker container |
| Firefox (geckodriver)   | 113+          | Y       | Need to add the host ip, e.g. "--host 123.45.6.78" |
| Google Chrome           | 113+          | Y       | Need to inform the allowed ips to connect, e.g "--allowed-ips=123.45.6.78" |
| Opera                   | 99+           | Y       | Need to inform the allowed ips to connect, e.g "--allowed-ips=123.45.6.78". Similar to Google Chrome |
| WinAppDriver            | 1.2.1+        | Y       | Need to define the host ip, e.g. "WinApppage.exe 10.0.0.10 4723" |
| Winium Desktop          | 1.6.0+        | Y       | Accepts remote calls by default |

* Accepts remote requests when running as servers

# Simple start
Install the lastest version of **Caqui**

```bash
pip install caqui
```

# Version 2.0.0+
In version 2.0.0+ it is possible to use Python objects similarly to Selenium. Example:

```python
from pytest import mark, fixture
from tests.constants import PAGE_URL
from caqui.easy import AsyncPage
from caqui.by import By
from caqui import synchronous
from caqui.easy.capabilities import ChromeOptionsBuilder
from caqui.easy.options import ChromeOptionsBuilder
from caqui.easy.server import Server
from time import sleep

SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"
PAGE_URL = "file:///sample.html"

@fixture(autouse=True, scope="session")
def setup_server():
    server = Server.get_instance(port=SERVER_PORT)
    server.start()
    yield
    sleep(3)
    server.dispose()

@fixture
def setup_environment():
    server_url = SERVER_URL
    options = ChromeOptionsBuilder().args(["headless"]).to_dict()
    capabilities = ChromeCapabilitiesBuilder().accept_insecure_certs(True).add_options(options).to_dict()
    page = AsyncPage(server_url, capabilities, PAGE_URL)
    yield page
    page.quit()

@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(setup_environment: AsyncPage):
    page = setup_environment
    await page.get(PAGE_URL)

    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = await page.find_element(locator_type, locator_value)
    assert await page.switch_to.frame(element_frame) is True

    alert_button_frame = await page.find_element(locator_type, locator_value_alert_frame)
    assert await alert_button_frame.click() is True
    assert await page.switch_to.alert.dismiss() is True

    assert await page.switch_to.default_content() is True
    alert_button_parent = await page.find_element(locator_type, locator_value_alert_parent)
    assert await alert_button_parent.get_attribute("any") == "any"
    assert await alert_button_parent.click() is True

```

## Running as multitasking

To execute the test in multiple tasks, use [pytest-async-cooperative](https://github.com/willemt/pytest-asyncio-cooperative). It will speed up the execution considerably.

```python
@mark.asyncio_cooperative
async def test_save_screenshot(setup_environment: AsyncPage):
    page = setup_environment
    assert await page.save_screenshot("/tmp/test.png") is True

@mark.asyncio_cooperative
async def test_object_to_string(setup_environment: AsyncPage):
    page = setup_environment
    element_string = synchronous.find_element(page.remote, page.session, By.XPATH, "//button")
    element = await page.find_element(locator=By.XPATH, value="//button")
    assert str(element) == element_string

```

## Running as multiprocessing
To run the tests in multiple processes use [pytest-xdist](https://github.com/pytest-dev/pytest-xdist). The execution is even faster than running in multiple tasks. Check this article [Supercharge Your Web Crawlers with Caqui: Boosting Speed with Multi-Processing](https://medium.com/@douglas.dcm/speed-up-your-web-crawlers-at-90-148f3ca97b6) to know how to increase the velocity of the executions in 90%.

```python
@mark.asyncio
async def test_save_screenshot(setup_environment: AsyncPage):
    page = setup_environment
    assert await page.save_screenshot("/tmp/test.png") is True

@mark.asyncio
async def test_object_to_string(setup_environment: AsyncPage):
    page = setup_environment
    element_string = synchronous.find_element(page.remote, page.session, By.XPATH, "//button")
    element = await page.find_element(locator=By.XPATH, value="//button")
    assert str(element) == element_string

```

# Driver as a server
In case you are using Appium, Winium or other driver not started by the library, just start the driver as a server.

For example. Download the same [ChromeDriver](https://chromepage.chromium.org/downloads) version as your installed Chrome and start the Driver as a server using the port "9999"

```bash
$ ./chromedriver --port=9999
Starting ChromeDriver 94.0.4606.61 (418b78f5838ed0b1c69bb4e51ea0252171854915-refs/branch-heads/4606@{#1204}) on port 9999
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.
```
# Webdriver Manager

Caqui depends on [Webdriver Manager](https://pypi.org/project/webdriver-manager/) that can be configured independenly and has some limitations. Check the project documentation for more information.


# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/caqui/blob/main/docs/CODE_OF_CONDUCT.md) before push new Merge Requests.
Now, follow the steps in [Contributing](https://github.com/douglasdcm/caqui/blob/main/docs/CONTRIBUTING.md) session.
