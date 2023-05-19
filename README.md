# Caqui 0.0.1 - Work in progress

**Caqui** is intended to command executions against Drivers asynchronously and in parallel. It launches the Driver as a server and sends requests to it. The intention is that the user does not worry about which Driver he/she is using. It can be **Web**Drivers like [Selenium](https://www.selenium.dev/), **Mobile**Drivers like [Appium](http://appium.io/docs/en/2.0/), or **Desktop**Drivers like [Winium](https://github.com/2gis/Winium.Desktop).

The process **Caqui** follows is similar of the one described in this [article](https://medium.com/@douglas.dcm/testing-windows-apps-with-http-rest-b4e8f80f8b7e) that experiments Drivers as servers together with [Jmeter](https://jmeter.apache.org/) to test Windows Calculator. However, the motivation to create **Caqui** was feed by the inspiration in [Arsenic](https://github.com/HENNGE/arsenic) library.

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
