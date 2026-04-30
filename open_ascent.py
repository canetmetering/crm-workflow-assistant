import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

ASCENT_URL = "https://app.ascentos.ai"
ASCENT_EMAIL = os.getenv("ASCENT_EMAIL")
ASCENT_PASSWORD = os.getenv("ASCENT_PASSWORD")


def is_logged_in(page):
    try:
        page.wait_for_selector(
            "input[type='email']",
            timeout=3000
        )
        return False
    except Exception:
        return True


def logout_ascent(page):
    print("Logging out of existing session...", flush=True)

    try:
        page.locator("button[aria-label='menu'], .hamburger, [class*='hamburger'], [class*='MenuIcon']").first.click(timeout=3000)
        page.wait_for_timeout(1000)
        page.get_by_text("Logout").click(timeout=3000)
        page.wait_for_timeout(2000)
        print("Logged out.", flush=True)
    except Exception as e:
        print(f"Logout via menu failed, trying direct: {e}", flush=True)
        try:
            page.locator("text=Logout").click(timeout=3000)
            page.wait_for_timeout(2000)
            print("Logged out via direct click.", flush=True)
        except Exception as e2:
            print(f"Logout failed entirely: {e2}", flush=True)


def login_ascent(page):
    print("Logging into AscentOS...", flush=True)

    try:
        page.wait_for_selector("input[type='email']", timeout=10000)
        page.fill("input[type='email']", ASCENT_EMAIL)
        page.fill("input[type='password']", ASCENT_PASSWORD)
        page.click("button[type='submit'], button:has-text('LOG IN')")
        page.wait_for_timeout(4000)
        print("Login submitted.", flush=True)
        return True
    except Exception as e:
        print(f"Login failed: {e}", flush=True)
        return False


def open_ascent_and_login(context):
    page = context.pages[0] if context.pages else context.new_page()

    try:
        page.bring_to_front()
    except Exception:
        pass

    page.goto(ASCENT_URL, wait_until="domcontentloaded", timeout=60000)
    page.set_viewport_size({"width": 1600, "height": 900})

    if is_logged_in(page):
        print("Already logged in — logging out first...", flush=True)
        logout_ascent(page)
        page.goto(ASCENT_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

    success = login_ascent(page)

    if not success:
        print("Auto-login failed. Please log in manually.", flush=True)
        input("Press Enter when logged in...")

    print("AscentOS ready.", flush=True)
