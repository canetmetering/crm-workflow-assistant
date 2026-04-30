import subprocess
import time
import os

CHROME_PATH = "/home/codespace/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"


def wait_for_display(display=":99", timeout=15):
    print("Waiting for display to be ready...", flush=True)
    start = time.time()
    while time.time() - start < timeout:
        result = subprocess.run(
            f"DISPLAY={display} xdpyinfo",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            print("Display ready.", flush=True)
            return True
        time.sleep(1)
    print("Display never became ready.", flush=True)
    return False


def launch_chrome_with_debugging():
    print("Launching Chrome with remote debugging on port 9222...", flush=True)

    wait_for_display()

    subprocess.Popen(
        f"DISPLAY=:99 {CHROME_PATH} "
        "--remote-debugging-port=9222 "
        "--no-sandbox "
        "--disable-dev-shm-usage "
        "--disable-gpu "
        "--window-size=1600,900 "
        "about:blank",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Waiting for Chrome to start...", flush=True)
    time.sleep(6)
    print("Chrome ready.", flush=True)


if __name__ == "__main__":
    launch_chrome_with_debugging()
