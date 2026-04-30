import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

JOBFLO_URL = "https://app.jobflo.co"
JOBFLO_EMAIL = os.getenv("JOBFLO_EMAIL")
JOBFLO_PASSWORD = os.getenv("JOBFLO_PASSWORD")


def is_logged_in(page):
    try:
        page.wait_for_selector(
            "input[type='email']",
            timeout=3000
        )
        return False
    except Exception:
        return True


def logout_jobflo(page):
    print("Logging out of existing session...", flush=True)

    try:
        page.locator("svg[data-testid='PersonIcon'], [aria-label='account'], button:last-child").last.click(timeout=3000)
        page.wait_for_timeout(1000)
        page.get_by_text("Logout").click(timeout=3000)
        page.wait_for_timeout(2000)
        print("Logged out.", flush=True)
        return True
    except Exception:
        pass

    try:
        page.goto(
            "https://app.jobflo.co/logout",
            wait_until="domcontentloaded",
            timeout=10000
        )
        page.wait_for_timeout(2000)
        print("Logged out via URL.", flush=True)
        return True
    except Exception as e:
        print(f"Logout failed: {e}", flush=True)
        return False


def login_jobflo(page):
    print("Logging into JobFlo...", flush=True)

    try:
        page.wait_for_selector("input[type='email']", timeout=10000)
        page.fill("input[type='email']", JOBFLO_EMAIL)
        page.fill("input[type='password']", JOBFLO_PASSWORD)
        page.click("button:has-text('Sign In')")
        page.wait_for_timeout(4000)
        print("Login submitted.", flush=True)
        return True
    except Exception as e:
        print(f"Login failed: {e}", flush=True)
        return False


def open_jobflo_and_login(context):
    page = context.pages[0] if context.pages else context.new_page()

    try:
        page.bring_to_front()
    except Exception:
        pass

    page.goto(JOBFLO_URL, wait_until="domcontentloaded", timeout=60000)
    page.set_viewport_size({"width": 1600, "height": 900})

    try:
        page.evaluate('document.body.style.zoom = "0.80"')
    except Exception:
        pass

    if is_logged_in(page):
        print("Already logged in — logging out first...", flush=True)
        logout_jobflo(page)
        page.goto(JOBFLO_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

    success = login_jobflo(page)

    if not success:
        print("Auto-login failed. Please log in manually.", flush=True)
        input("Press Enter when logged in...")

    print("Navigating to customers page...", flush=True)
    page.goto(
        "https://app.jobflo.co/customers",
        wait_until="domcontentloaded",
        timeout=60000
    )
    page.wait_for_timeout(2000)
    print("Customers page loaded.", flush=True)


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        open_jobflo_and_login(context)
        print("Done. Browser staying open.")
        input("Press Enter to exit...")
