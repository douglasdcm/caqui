# Caqui

[![Python application](https://github.com/douglasdcm/caqui/actions/workflows/python-app.yml/badge.svg)](https://github.com/douglasdcm/caqui/actions/workflows/python-app.yml)
[![PyPI Downloads](https://static.pepy.tech/badge/caqui)](https://pepy.tech/projects/caqui)

**Caqui** is a Python library for browser, mobile, and desktop automation that works with any driver that exposes a WebDriver-style REST API. It lets you send commands **synchronously or asynchronously**, and you don’t need to think about which underlying driver you’re using.

Caqui is designed for developers who want a unified automation API that can run:

* WebDriver (Chrome, Firefox, Opera, Edge)
* Appium (Android, iOS)
* Winium / WinAppDriver (Windows desktop applications)
* Any remote WebDriver-compatible server

Caqui runs seamlessly on a local machine or across remote hosts, and supports both **multitasking with asyncio** and **multiprocessing** for high-throughput use cases such as parallel testing, web scraping, or distributed automation.

---

# Supported Drivers

| WebDriver             | Version | Remote* | If remote                                                       |
| --------------------- | ------- | ------- | ------------------------------------------------------------- |
| Appium                | 2.0.0+  | Y       | Accepts remote calls by default. Tested with Appium in Docker |
| Firefox (geckodriver) | 113+    | Y       | Requires defining the host IP, e.g. `--host 123.45.6.78`      |
| Google Chrome         | 113+    | Y       | Requires allowed IPs, e.g. `--allowed-ips=123.45.6.78`        |
| Opera                 | 99+     | Y       | Same restrictions as Chrome                                   |
| WinAppDriver          | 1.2.1+  | Y       | Requires host IP, e.g. `WinApppage.exe 10.0.0.10 4723`        |
| Winium Desktop        | 1.6.0+  | Y       | Accepts remote calls by default                               |

*Remote = can accept REST requests when running as a server.

---

# Installation

```bash
pip install caqui
```

---

# Using Caqui 2.0.0+

From version **2.0.0+**, Caqui includes a high-level API that mirrors Selenium’s object model and exposes async methods for browser, mobile, and desktop automation.
[Full documentation:](https://caqui.readthedocs.io/en/latest/caqui.html)

Example:

```python
from os import getcwd
from pytest import mark, fixture
from caqui.easy.drivers import AsyncDriver
from caqui.easy.capabilities import ChromeCapabilitiesBuilder
from caqui.by import By
from caqui.easy.server import LocalServer

BASE_DIR = getcwd()
PAGE_URL = f"file:///{BASE_DIR}/html/playground.html"
SERVER_PORT = 9999
SERVER_URL = f"http://localhost:{SERVER_PORT}"


@fixture(autouse=True, scope="session")
def setup_server():
    server = LocalServer(port=SERVER_PORT)
    server.start_chrome()
    yield
    server.dispose(delay=3)


@fixture
def caqui_driver():
    server_url = SERVER_URL
    capabilities = (
        ChromeCapabilitiesBuilder().accept_insecure_certs(True).args(["headless"])
    )
    page = AsyncDriver(server_url, capabilities)
    yield page
    page.quit()


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(caqui_driver: AsyncDriver):
    await caqui_driver.get(PAGE_URL)
    element_frame = await caqui_driver.find_element(By.ID, "my-iframe")
    assert await caqui_driver.switch_to.frame(element_frame)

    alert_button_frame = await caqui_driver.find_element(By.ID, "alert-button-iframe")
    await alert_button_frame.click()
    await caqui_driver.switch_to.alert.dismiss()

    await caqui_driver.switch_to.default_content()
    alert_button_parent = await caqui_driver.find_element(By.ID, "alert-button")
    assert await alert_button_parent.get_attribute("any") == "any"
    await alert_button_parent.click()

```

---

# Running Tests with Multitasking

Caqui supports asyncio out of the box.
To run multiple async tests concurrently, use **pytest-async-cooperative**:

```python
@mark.asyncio_cooperative
async def test_save_screenshot(caqui_driver: AsyncDriver):
    await caqui_driver.get(PAGE_URL)
    assert await caqui_driver.save_screenshot("/tmp/test.png")


@mark.asyncio_cooperative
async def test_click(caqui_driver: AsyncDriver):
    await caqui_driver.get(PAGE_URL)
    element = await caqui_driver.find_element(By.XPATH, "//button")
    await element.click()
```

Running tests this way significantly reduces execution time, especially when interacting with multiple drivers or sessions.

---

# Running Tests with Multiprocessing

If your workloads benefit from multiple processes, Caqui also works with **pytest-xdist**.
This approach is often faster than cooperative multitasking.

A guide to optimizing performance (including a real benchmark):
[Speed up your web crawlers at 90%](https://medium.com/@douglas.dcm/speed-up-your-web-crawlers-at-90-148f3ca97b6)

Example:

```python
@mark.asyncio
async def test_save_screenshot(caqui_driver: AsyncDriver):
    await caqui_driver.get(PAGE_URL)
    assert await caqui_driver.save_screenshot("/tmp/test.png")


@mark.asyncio
async def test_click(caqui_driver: AsyncDriver):
    await caqui_driver.get(PAGE_URL)
    element = await caqui_driver.find_element(By.XPATH, "//button")
    await element.click()

```

---

# Running a Driver as a Server

If you use external drivers such as Appium, Winium, or a standalone ChromeDriver, run them as servers and point Caqui to their URL.

Example for ChromeDriver on port 9999:

```bash
$ ./chromedriver --port=9999
Starting ChromeDriver 94.0.4606.61 (418b78f5838ed0b1c69bb4e51ea0252171854915-refs/branch-heads/4606@{#1204}) on port 9999
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.
```

---

# WebDriver Manager

Caqui’s `LocalServer` class uses [Webdriver Manager](https://pypi.org/project/webdriver-manager/).
The tool comes with its own constraints.
Check its documentation for details if you need custom driver handling.

---

# Contributing

Before submitting a pull request, review the project guidelines:
Code of Conduct:
[CODE OF CONDUCT](https://github.com/douglasdcm/caqui/blob/main/docs/CODE_OF_CONDUCT.md)

Contribution Guide:
[CONTRIBUTING](https://github.com/douglasdcm/caqui/blob/main/docs/CONTRIBUTING.md)

Contributions, issue reports, and performance feedback are welcome.
