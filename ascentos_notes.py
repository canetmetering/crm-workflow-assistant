def open_notes(project_page):
    print("Trying to open Notes...")

    buttons = project_page.locator("button")
    button_count = buttons.count()

    # Working older method: open menu, click Notes text
    for b in range(button_count - 1, max(button_count - 12, -1), -1):
        try:
            buttons.nth(b).click(timeout=2000, force=True)
            project_page.wait_for_timeout(1000)

            notes_locator = project_page.locator("text=Notes")

            if notes_locator.count() > 0:
                notes_locator.nth(0).evaluate("el => el.click()")
                project_page.wait_for_timeout(3000)
                print(f"Opened Notes using menu button #{b}")
                return True

        except Exception:
            pass

    # Fallback: click Notes if already visible
    try:
        notes_locator = project_page.locator("text=Notes")

        if notes_locator.count() > 0:
            notes_locator.nth(0).evaluate("el => el.click()")
            project_page.wait_for_timeout(3000)
            print("Opened Notes using direct click")
            return True

    except Exception:
        pass

    # Fallback: escape and retry
    try:
        project_page.keyboard.press("Escape")
        project_page.wait_for_timeout(1000)

        buttons = project_page.locator("button")
        button_count = buttons.count()

        for b in range(button_count - 1, max(button_count - 12, -1), -1):
            try:
                buttons.nth(b).click(timeout=2000, force=True)
                project_page.wait_for_timeout(1000)

                notes_locator = project_page.locator("text=Notes")

                if notes_locator.count() > 0:
                    notes_locator.nth(0).evaluate("el => el.click()")
                    project_page.wait_for_timeout(3000)
                    print(f"Opened Notes after fallback using button #{b}")
                    return True

            except Exception:
                pass

    except Exception:
        pass

    print("FAILED: Could not open Notes.")
    return False


def scrape_notes(project_page):
    notes_opened = open_notes(project_page)

    if not notes_opened:
        return "NO NOTES FOUND / COULD NOT OPEN NOTES"

    print("Loading raw notes/page text...")

    for _ in range(8):
        project_page.mouse.wheel(0, 5000)
        project_page.wait_for_timeout(1000)

    raw_text = project_page.locator("body").inner_text()

    print(f"Raw notes/page text length: {len(raw_text)}")

    return raw_text