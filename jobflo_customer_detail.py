from jobflo_tab_manager import wait_for_new_customer_tab
from jobflo_header_extractor import extract_customer_header
from jobflo_notes_scraper import scrape_jobflo_notes, filter_notes_by_timeframe


def open_notes_tab(page):
    print("Opening JobFlo notes tab...", flush=True)

    try:
        page.get_by_role("tab", name="Notes").click(timeout=5000)
        page.wait_for_timeout(2000)
        return True
    except Exception:
        pass

    try:
        page.locator("text=Notes").first.click(timeout=5000)
        page.wait_for_timeout(2000)
        return True
    except Exception:
        pass

    print("FAILED: Could not open Notes tab.", flush=True)
    return False
