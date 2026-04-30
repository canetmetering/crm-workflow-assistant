def recover_registry_page(page):
    """
    Browser recovery failsafe:
    If the project tab crashes or the registry gets stale,
    refresh the registry page and wait for rows to reload.
    """

    print("Browser recovery: refreshing registry page...")

    page.reload(
        wait_until="domcontentloaded",
        timeout=30000
    )

    page.wait_for_timeout(5000)

    rows = page.locator("tbody tr")
    row_count = rows.count()

    if row_count == 0:
        raise Exception(
            "Browser recovery failed: registry rows did not reload."
        )

    print(f"Browser recovery complete. Registry rows found: {row_count}")

    return page