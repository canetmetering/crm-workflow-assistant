from browser_recovery import recover_registry_page


def close_extra_tabs(context, keep_page=None):
    pages = list(context.pages)

    if not pages:
        return None

    if keep_page is None:
        keep_page = pages[0]

    for page in pages:
        if page == keep_page:
            continue

        try:
            page.close()
        except Exception:
            pass

    try:
        keep_page.bring_to_front()
    except Exception:
        pass

    return keep_page


def wait_for_registry_rows(page, timeout_ms=20000):
    print("Waiting for registry rows to load...", flush=True)

    rows = page.locator("tbody tr")
    rows.first.wait_for(
        state="visible",
        timeout=timeout_ms
    )

    page.wait_for_timeout(1500)


def open_registry_clean(context, registry_url):
    page = context.new_page()

    page.goto(
        registry_url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    try:
        wait_for_registry_rows(page)

    except Exception as error:
        print(f"Registry load failed: {error}", flush=True)
        print("Running browser recovery...", flush=True)

        page = recover_registry_page(page)

        wait_for_registry_rows(page)

    close_extra_tabs(
        context,
        keep_page=page
    )

    return page