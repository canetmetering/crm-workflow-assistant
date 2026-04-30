import os
import sys
from playwright.sync_api import sync_playwright
from ascent_workflow import run_ascent_workflow
from jobflo_workflow import run_jobflo_workflow
from open_ascent import open_ascent_and_login
from open_jobflo import open_jobflo_and_login


CHROME_PATH = "/root/.cache/ms-playwright/chromium-1148/chrome-linux64/chrome"


def start_virtual_display():
    import subprocess
    import time

    subprocess.Popen(
        "Xvfb :99 -screen 0 1920x1080x24",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)

    subprocess.Popen(
        "DISPLAY=:99 fluxbox",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)


def launch_chrome():
    import subprocess
    import time

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
    time.sleep(6)


def main():
    platform = os.getenv("WORKFLOW_PLATFORM")
    timeframe = os.getenv("WORKFLOW_TIMEFRAME")

    if not platform or not timeframe:
        print("ERROR: Missing platform or timeframe", flush=True)
        sys.exit(1)

    print(f"Starting {platform} workflow - timeframe: {timeframe}", flush=True)

    start_virtual_display()
    launch_chrome()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]

        if platform == "ascent":
            open_ascent_and_login(context)
            run_ascent_workflow(context, timeframe=timeframe)

        elif platform == "jobflo":
            open_jobflo_and_login(context)
            run_jobflo_workflow(context, timeframe=timeframe)

    print("Workflow complete.", flush=True)


if __name__ == "__main__":
    main()
