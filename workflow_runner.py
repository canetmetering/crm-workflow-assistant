import os
import sys
from playwright.sync_api import sync_playwright
from ascent_workflow import run_ascent_workflow
from jobflo_workflow import run_jobflo_workflow
from open_ascent import open_ascent_and_login
from open_jobflo import open_jobflo_and_login


def main():
    platform = os.getenv("WORKFLOW_PLATFORM")
    timeframe = os.getenv("WORKFLOW_TIMEFRAME")

    if not platform or not timeframe:
        print("ERROR: Missing platform or timeframe", flush=True)
        sys.exit(1)

    print(f"Starting {platform} workflow - timeframe: {timeframe}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1600,900",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-extensions",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            java_script_enabled=True,
            ignore_https_errors=True,
        )

        # Remove webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        if platform == "ascent":
            open_ascent_and_login(context)
            run_ascent_workflow(context, timeframe=timeframe)

        elif platform == "jobflo":
            open_jobflo_and_login(context)
            run_jobflo_workflow(context, timeframe=timeframe)

        context.close()
        browser.close()

    print("Workflow complete.", flush=True)


if __name__ == "__main__":
    main()
