# Caqui

**Caqui** is intended to command executions against Drivers synchronously and asynchronously. Launch the Driver as a server and send requests to it. The intention is that the user does not worry about which Driver he/she is using. It can be **Web**Drivers like [Selenium](https://www.selenium.dev/), **Mobile**Drivers like [Appium](http://appium.io/docs/en/2.0/), or **Desktop**Drivers like [Winium](https://github.com/2gis/Winium.Desktop).

The process **Caqui** follows is similar of the one described in this [article](https://medium.com/@douglas.dcm/testing-windows-apps-with-http-rest-b4e8f80f8b7e) that experiments Drivers as servers together with [Jmeter](https://jmeter.apache.org/) to test the Windows Calculator. However, the motivation to create **Caqui** was feed by the inspiration in [Arsenic](https://github.com/HENNGE/arsenic) library.

**Caqui** is planned to be Driver agnostic, so the user can start any Driver as a server and just inform the server URL. Hence, the code is decoupled from the chosen Driver.

**Caqui** can be used in remote calls. As it needs just the server URL, the user can start the Driver as a server in any host and provide the URL to **Caqui** clients.

# Tested WebDrivers

| WebDriver               | Version       | Remote* | Comment |
| ----------------------- | ------------- | ------- |-------- |
| Appium                  | 2.0.0         | Y       | Accepts remote calls by default. Tested with Appium in Docker container |
| Firefox (geckodriver)   | 113           | Y       | Need to add the host ip, e.g. "--host 123.45.6.78" |
| Google Chrome           | 113+          | Y       | Need to inform allowed ips to connect, e.g "--allowed-ips=123.45.6.78" |
| Opera                   | 99            | Y       | Need to inform allowed ips to connect, e.g "--allowed-ips=123.45.6.78". Similar to Google Chrome |
| WinAppDriver            | 1.2.1         | Y       | Need to define the host ip, e.g. "WinAppDriver.exe 10.0.0.10 4723" |
| Winium Desktop          | 1.6.0         | Y       | Accepts remote calls by default |

* Accepts remote requests when running as servers

# Simple start
Install the lastest version of **Caqui**

```
pip install caqui
```

Download the same [ChromeDriver](https://chromedriver.chromium.org/downloads) version as your installed Chrome and start the Driver as a server using the port "9999"

```
$ ./chromedriver --port=9999
Starting ChromeDriver 94.0.4606.61 (418b78f5838ed0b1c69bb4e51ea0252171854915-refs/branch-heads/4606@{#1204}) on port 9999
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.
```

Given the HTML content in `playground.html`

```
<html>

<head>
    <title>Sample page</title>
</head>

<body>
    <h1>Basic page</h1>
    <p> This is a sample page to be used to sanity check </p>
    <input id="input">
    <button id="button" onclick="myFunction(this, 'red')">test</button>
    <p id="end">end</p>
    <a src="http://any1.com" id="a1">any1.com</a>
    <a src="http://any2.com" id="a2">any2.com</a>
    <a src="http://any3.com" id="a3">any3.com</a>
    <a src="http://any4.com" id="a4">any4.com</a>

    <script>
        function myFunction(element, color) {
            element.style.color = color;
        }
    </script>
</body>

</html>
```

And the code in `sample.py` file
```
import asyncio
import time
from caqui import synchronous, asynchronous
from os import getcwd
from tests.constants import PAGE_URL
from caqui.easy.capabilities import CapabilitiesBuilder

BASE_DIR = getcwd()

MAX_CONCURRENCY = 5  # number of webdriver instances running
sem = asyncio.Semaphore(MAX_CONCURRENCY)


async def get_all_links():
    async with sem:
        driver_url = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()

        session = await asynchronous.get_session(driver_url, capabilities)
        await asynchronous.go_to_page(
            driver_url,
            session,
            PAGE_URL,
        )

        for i in range(4):
            i += 1
            locator_value = f"//a[@id='a{i}']"
            locator_type = "xpath"
            anchors = []

            anchors = await asynchronous.find_elements(
                driver_url, session, locator_type, locator_value
            )
            print(f"Found {len(anchors)} links")

        for anchor in anchors:
            text = await asynchronous.get_property(driver_url, session, anchor, "href")
            print(f"Link found '{text}'")

        synchronous.close_session(driver_url, session)


# Reference: https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
async def main():
    number_of_websites = range(10)
    tasks = [asyncio.ensure_future(get_all_links()) for number in number_of_websites]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        end = time.time()
        print(f"Time: {end-start:.2f} sec")

```

Run the file
```
python sample.py
```
Output
```
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Found 1 links
Found 1 links
Found 1 links
Found 1 links
Link found 'http://any4.com/'
Time: 5.01 sec

```
# Version 2.0.0
In version 2 it is possible to use Python objects similarly to Selenium. Example:

```
from caqui.easy import AsyncDriver
from caqui.by import By
from caqui import synchronous
from tests.constants import PAGE_URL
from pytest import mark, fixture
from caqui.easy.capabilities import CapabilitiesBuilder


@fixture
def __setup():
    remote = "http://127.0.0.1:9999"
    capabilities = (
        CapabilitiesBuilder()
        .browser_name("chrome")
        .accept_insecure_certs(True)
        .page_load_strategy("normal")
        .addtional_capability(
            {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
        )
    ).build()
    driver = AsyncDriver(remote, capabilities, PAGE_URL)
    yield driver
    driver.quit()


@mark.asyncio
async def test_switch_to_parent_frame_and_click_alert(__setup: AsyncDriver):
    driver = __setup
    await driver.get(PAGE_URL)

    locator_type = "id"
    locator_value = "my-iframe"
    locator_value_alert_parent = "alert-button"
    locator_value_alert_frame = "alert-button-iframe"

    element_frame = await driver.find_element(locator_type, locator_value)
    assert await driver.switch_to.frame(element_frame) is True

    alert_button_frame = await driver.find_element(
        locator_type, locator_value_alert_frame
    )
    assert await alert_button_frame.click() is True
    assert await driver.switch_to.alert.dismiss() is True

    assert await driver.switch_to.default_content() is True
    alert_button_parent = await driver.find_element(
        locator_type, locator_value_alert_parent
    )
    assert await alert_button_parent.get_attribute("any") == "any"
    assert await alert_button_parent.click() is True


("style")
    assert "display: none;" == await hidden_button.get_attribute("style")

```

## Running as multitasking

To execute the test in multiple tasks, use [pytest-async-cooperative](https://github.com/willemt/pytest-asyncio-cooperative). It will speed up the execution considerably.

```
from caqui.easy import AsyncDriver, ActionChains
from caqui.by import By
from pytest import mark, fixture
from tests.constants import PAGE_URL
from caqui import synchronous
from caqui.easy.capabilities import CapabilitiesBuilder


class TestObject:
    @fixture
    def setup(self):
        remote = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        driver = AsyncDriver(remote, capabilities, PAGE_URL)
        yield driver
        driver.quit()

    @mark.asyncio_cooperative
    async def test_save_screenshot(self, setup: AsyncDriver):
        driver = setup

        assert await driver.save_screenshot("/tmp/test.png") is True

    @mark.asyncio_cooperative
    async def test_object_to_string(self, setup: AsyncDriver):
        driver = setup

        element_string = synchronous.find_element(
            driver.remote, driver.session, By.XPATH, "//button"
        )
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == element_string

```

## Running as multiprocessing
To run the tests in multiple processes use [pytest-xdist](https://github.com/pytest-dev/pytest-xdist). The execution is even faster than running in multiple tasks. Check this article [Supercharge Your Web Crawlers with Caqui: Boosting Speed with Multi-Processing](https://medium.com/@douglas.dcm/speed-up-your-web-crawlers-at-90-148f3ca97b6) to know how to increase the velocity of the executions in 90%.

```
from caqui.easy import AsyncDriver, ActionChains
from caqui.by import By
from pytest import mark, fixture
from tests.constants import PAGE_URL
from caqui import synchronous
from caqui.easy.capabilities import CapabilitiesBuilder
import asyncio


class TestObject:
    @fixture
    def setup(self):
        remote = "http://127.0.0.1:9999"
        capabilities = (
            CapabilitiesBuilder()
            .browser_name("chrome")
            .accept_insecure_certs(True)
            .additional_capability(
                {"goog:chromeOptions": {"extensions": [], "args": ["--headless"]}}
            )
        ).build()
        driver = AsyncDriver(remote, capabilities, PAGE_URL)
        yield driver
        driver.quit()

    @mark.asyncio
    async def test_save_screenshot(self, setup: AsyncDriver):
        driver = setup

        assert await driver.save_screenshot("/tmp/test.png") is True

    @mark.asyncio
    async def test_object_to_string(self, setup: AsyncDriver):
        driver = setup

        element_string = synchronous.find_element(
            driver.remote, driver.session, By.XPATH, "//button"
        )
        element = await driver.find_element(locator=By.XPATH, value="//button")
        assert str(element) == element_string

```

# Driver as server
To illustrate what I mean by "Driver as server", lets get [chromedriver](https://chromedriver.chromium.org/home) and execute it as an ordinary shell script file.

```
./chromedriver --port=9999
Starting ChromeDriver 94.0.4606.61 (418b78f5838ed0b1c69bb4e51ea0252171854915-refs/branch-heads/4606@{#1204}) on port 9999
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully.

```
Notice the Driver is running and waiting for HTTP requests.

Lets open a new session against it
```
curl --location '127.0.0.1:9999/session' \
--header 'Content-Type: application/json' \
--data '{
    "desiredCapabilities": {
        "browserName": "firefox",
        "marionette": true,
        "acceptInsecureCerts": true
    }
}'
```
Here is the response returned
```
{
    "sessionId": "b6654121c4ba1e8395ded73a27b7d8f5",
    "status": 0,
    "value": {
        "acceptInsecureCerts": true,
        "acceptSslCerts": true,
        "applicationCacheEnabled": false,
        "browserConnectionEnabled": false,
        "browserName": "chrome",
        "chrome": {
            "chromedriverVersion": "94.0.4606.61 (418b78f5838ed0b1c69bb4e51ea0252171854915-refs/branch-heads/4606@{#1204})",
            "userDataDir": "/tmp/.com.google.Chrome.xtZUOj"
        },
        "cssSelectorsEnabled": true,
        "databaseEnabled": false,
        "goog:chromeOptions": {
            "debuggerAddress": "localhost:44437"
        },
        "handlesAlerts": true,
        "hasTouchScreen": false,
        "javascriptEnabled": true,
        "locationContextEnabled": true,
        "mobileEmulationEnabled": false,
        "nativeEvents": true,
        "networkConnectionEnabled": false,
        "pageLoadStrategy": "normal",
        "platform": "Linux",
        "proxy": {},
        "rotatable": false,
        "setWindowRect": true,
        "strictFileInteractability": false,
        "takesHeapSnapshot": true,
        "takesScreenshot": true,
        "timeouts": {
            "implicit": 0,
            "pageLoad": 300000,
            "script": 30000
        },
        "unexpectedAlertBehaviour": "ignore",
        "version": "94.0.4606.54",
        "webStorageEnabled": true,
        "webauthn:extension:credBlob": true,
        "webauthn:extension:largeBlob": true,
        "webauthn:virtualAuthenticators": true
    }
}
```
The *sessionId* value can be used to perform further actions like *find element*, *send keys* or *click* buttons. More details can be found in [Json Wire Protocol Specification](https://www.selenium.dev/documentation/legacy/json_wire_protocol/).
Also with the *-h* parameter in Drivers, for example: 
```
./chromedriver -h

Usage: ./chromedriver [OPTIONS]

Options
  --port=PORT                     port to listen on
  --adb-port=PORT                 adb server port
  --log-path=FILE                 write server log to file instead of stderr, increases log level to INFO
  --log-level=LEVEL               set log level: ALL, DEBUG, INFO, WARNING, SEVERE, OFF
  --verbose                       log verbosely (equivalent to --log-level=ALL)
  --silent                        log nothing (equivalent to --log-level=OFF)
  --append-log                    append log file instead of rewriting
  --replayable                    (experimental) log verbosely and don't truncate long strings so that the log can be replayed.
  --version                       print the version number and exit
  --url-base                      base URL path prefix for commands, e.g. wd/url
  --readable-timestamp            add readable timestamps to log
  --enable-chrome-logs            show logs from the browser (overrides other logging options)
  --disable-dev-shm-usage         do not use /dev/shm (add this switch if seeing errors related to shared memory)
  --allowed-ips                   comma-separated allowlist of remote IP addresses which are allowed to connect to ChromeDriver
```
# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/caqui/blob/main/CODE_OF_CONDUCT.md) before push new Merge Requests.
Now, follow the steps in [Contributing](https://github.com/douglasdcm/caqui/blob/main/CONTRIBUTING.md) session.
