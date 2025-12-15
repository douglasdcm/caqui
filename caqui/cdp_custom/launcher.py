import subprocess
import time
import json
import urllib.request

def launch_chrome(port=9222):
    subprocess.Popen([
        "google-chrome",
        f"--remote-debugging-port={port}",
        "--user-data-dir=/tmp/cdp-profile",
        "--no-first-run",
        "--no-default-browser-check",
        # "--headless",
        "about:blank"
    ])
    time.sleep(1)
    return True

def close_chrome():
    subprocess.Popen([
        "pkill",
        "chrome"
    ])
    # time.sleep(1)

def get_ws_url(port=9222):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as r:
        targets = json.loads(r.read())
        return targets[0]["webSocketDebuggerUrl"]
