import time


def wait_for_new_customer_tab(context, original_tab_count, timeout_seconds=15):
    print("Waiting for customer tab...", flush=True)

    start = time.time()

    while True:
        if len(context.pages) > original_tab_count:
            new_page = context.pages[-1]
            new_page.wait_for_load_state("domcontentloaded")
            print("Customer tab detected.", flush=True)
            return new_page

        if time.time() - start > timeout_seconds:
            print("Timed out waiting for customer tab.", flush=True)
            return None

        time.sleep(0.5)
