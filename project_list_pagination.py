def go_to_next_project_list_page(list_page):
    buttons = list_page.locator("button")
    button_count = buttons.count()

    for b in range(button_count - 1, max(button_count - 12, -1), -1):
        try:
            button = buttons.nth(b)
            label = button.get_attribute("aria-label") or ""
            text = button.inner_text(timeout=1000).strip()

            if "next" in label.lower() or text in {">", "›"}:
                disabled = button.get_attribute("disabled")

                if disabled is not None:
                    return False

                button.click(timeout=2000, force=True)
                list_page.wait_for_timeout(3000)
                return True

        except Exception:
            pass

    return False