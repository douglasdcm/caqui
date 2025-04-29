# Simple example of usage of caqui with Android App
# It opens the app and get the source code
# Appium configured using docker for simplicity
# https://hub.docker.com/r/appium/appium/
# sample app in ./tests/apk folder
from caqui import synchronous


def main():
    server_url = "http://127.0.0.1:4723"
    capabilities = {
        "capabilities": {
            "firstMatch": [{}],
            "alwaysMatch": {
                "appium:automationName": "UIAutomator2",
                "platformName": "Android",
                "appium:udid": "YOUR-APP-UUID",  # replace with your device uuid
                # refereces the folder in docker container
                "appium:app": "/home/androidusr/sample.apk",
            },
        }
    }

    session = synchronous.get_session(server_url, capabilities)
    print("session: ", session)

    source = synchronous.get_page_source(server_url, session)
    print("source: ", source)

    synchronous.close_session(server_url, session)


if __name__ == "__main__":
    main()
