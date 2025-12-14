import orjson
import subprocess
import time
import urllib.request


def launch_chrome(port=9222):
    subprocess.Popen(
        [
            "google-chrome",
            f"--remote-debugging-port={port}",
            "--user-data-dir=/tmp/cdp-profile",
            "--no-first-run",
            "--no-default-browser-check",
            "--headless",
            "--no-zygote",
            "--no-sandbox",
            "about:blank",
        ]
    )
    time.sleep(0.1)
    return True


def close_chrome():
    subprocess.Popen(["pkill", "chrome"])


def get_ws_url(port=9222):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as r:
        targets = orjson.loads(r.read())
        return targets[0]["webSocketDebuggerUrl"]
