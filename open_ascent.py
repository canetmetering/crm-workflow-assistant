import os
from dotenv import load_dotenv

load_dotenv()

ASCENT_URL = "https://app.ascentos.ai"
ASCENT_EMAIL = os.getenv("ASCENT_EMAIL")
ASCENT_PASSWORD = os.getenv("ASCENT_PASSWORD")


def login_ascent(page):
    print("Logging into AscentOS...", flush=True)
    try:
        page.wait_for_timeout(5000)
        print(f"URL: {page.url}", flush=True)
        print(f"Title: {page.title()}", flush=True)

        # Print all input fields found
        inputs = page.locator("input").all()
        print(f"Input fields found: {len(inputs)}", flush=True)
        for i, inp in enumerate(inputs):
            try:
                print(f"Input {i}: type={inp.get_attribute('type')} name={inp.get_attribute('name')}", flush=True)
            except:
                pass

        page.wait_for_selector("input[type='email']", timeout=30000)
        print("Login form found.", flush=True)
        page.fill("input[type='email']", ASCENT_EMAIL)
        page.fill("input[type='password']", ASCENT_PASSWORD)
        page.click("button[type='submit'], button:has-text('LOG IN')")
        page.wait_for_timeout(5000)
        print("Login submitted.", flush=True)
        return True
    except Exception as e:
        print(f"Login failed: {e}", flush=True)
        return False


def open_ascent_and_login(context):
    page = context.new_page()
    page.set_viewport_size({"width": 1600, "height": 900})

    print("Opening AscentOS login page...", flush=True)
    page.goto(ASCENT_URL, wait_until="domcontentloaded", timeout=60000)

    success = login_ascent(page)

    if not success:
        print("Login failed — aborting.", flush=True)
        raise Exception("AscentOS login failed")

    print("AscentOS ready.", flush=True)
