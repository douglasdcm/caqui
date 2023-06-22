# Simple example of usage of caqui with Windows Calculator
# It opens the Calculator and clicks the number "8"
# Test works just in Windows environment. Tested with Windows 10
from caqui import synchronous


def main():
    driver_url = "http://127.0.0.1:4723"
    capabilities = {
        "capabilities": {
            "firstMatch": [{}],
            "alwaysMatch": {},
        },
        "desiredCapabilities": {
            "debugConnectToRunningApp": "false",
            "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
        },
    }
    session = synchronous.get_session(driver_url, capabilities)
    element = synchronous.find_element(
        driver_url, session, locator_type="name", locator_value="Eight"
    )

    synchronous.click(driver_url, session, element)
    synchronous.close_session(driver_url, session)


if __name__ == "__main__":
    main()
