from caqui.easy.options import ChromeOptionsBuilder, FirefoxOptions


def test_firefox_options():
    expected = {
        "moz:firefoxOptions": {
            "binary": "/usr/bin/firefox",
            "args": ["-headless", "-profile"],
            "env": {"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"},
            "log": {"level": "trace"},
            "profile": "any",
            "androidIntentArguments": ["a", "b"],
            "androidActivity": "any",
            "androidDeviceSerial": "any",
            "androidPackage": "any",
            "level": "info",
        }
    }
    options = (
        FirefoxOptions()
        .binary("/usr/bin/firefox")
        .args(["-headless", "-profile"])
        .env({"MOZ_LOG": "nsHttp:5", "MOZ_LOG_FILE": "/path/to/my/profile/log"})
        .log({"level": "trace"})
        .profile("any")
        .android_intent_arguments(["a", "b"])
        .android_activity("any")
        .android_device_serial("any")
        .android_package("any")
        .level("info")
    )
    assert options.to_dict() == expected


def test_chrome_options():
    expected = {
        "goog:chromeOptions": {
            "args": [
                "headless",
            ],
            "detach": True,
            "prefs": {"javascript.options.showInConsole": False},
            "binary": "/path/to/chrome/executable",
            "debuggerAddress": "127.0.0.1:9999",
            "detach": True,
            "excludeSwitches": [
                "sw1",
                "sw2",
            ],
            "extensions": [
                "ext1",
                "ext2",
            ],
            "localState": {
                "any": "any",
            },
            "minidumpPath": "any",
            "mobileEmulation": {
                "any": "any",
            },
            "perfLoggingPrefs": {
                "bufferUsageReportingInterval": 1000,
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
            },
            "windowsTypes": "any",
        }
    }
    options = options = (
        ChromeOptionsBuilder()
        .args(["headless"])
        .prefs({"javascript.options.showInConsole": False})
        .detach(True)
        .binary("/path/to/chrome/executable")
        .extensions(["ext1", "ext2"])
        .local_state({"any": "any"})
        .debugger_address("127.0.0.1:9999")
        .exclude_switches(["sw1", "sw2"])
        .minidump_path("any")
        .mobile_emulation({"any": "any"})
        .windows_types("any")
        .perf_logging_prefs(
            {
                "enableNetwork": False,
                "enablePage": False,
                "traceCategories": "devtools.network",
                "bufferUsageReportingInterval": 1000,
            }
        )
    )
    assert options.to_dict() == expected
