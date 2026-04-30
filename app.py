import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from platform_selector import choose_platform
from ascent_workflow import run_ascent_workflow
from jobflo_workflow import run_jobflo_workflow
from boot_ascent_environment import boot_ascent_environment
from boot_jobflo_environment import boot_jobflo_environment
from open_ascent import open_ascent_and_login
from open_jobflo import open_jobflo_and_login

load_dotenv()


def main():
    platform = choose_platform()

    if not platform:
        print("No platform selected.", flush=True)
        return

    platform = platform.strip().lower()

    if platform == "ascent":
        boot_ascent_environment()

        print("\nOpen Codespaces PORTS → 6080 → vnc_auto.html", flush=True)
        input("Press Enter when browser is open and ready...")

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            open_ascent_and_login(context)
            run_ascent_workflow(context)

    elif platform == "jobflo":
        boot_jobflo_environment()

        print("\nOpen Codespaces PORTS → 6080 → vnc_auto.html", flush=True)
        input("Press Enter when browser is open and ready...")

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            open_jobflo_and_login(context)
            run_jobflo_workflow(context)

    else:
        print(f"Invalid platform: {platform}", flush=True)


if __name__ == "__main__":
    main()
