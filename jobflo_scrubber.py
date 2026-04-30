from jobflo_customer_opener import open_customer_in_new_tab
from jobflo_customer_detail import (
    extract_customer_header,
    open_notes_tab,
    scrape_jobflo_notes,
    filter_notes_by_timeframe
)


TIMEFRAME_MAP = {
    "48h": 2,
    "week": 7,
    "full": 9999,
}


def scrub_jobflo_customers(context, customers, timeframe):
    relevant_customers = []

    registry_page = context.pages[0]

    for customer in customers:
        print(f"\nOpening {customer['customer_name']}...", flush=True)

        try:
            with context.expect_page(timeout=15000) as new_page_info:
                open_customer_in_new_tab(customer, registry_page)

            customer_page = new_page_info.value
            customer_page.wait_for_load_state("domcontentloaded")
            print("Customer tab detected.", flush=True)

        except Exception as e:
            print(
                f"Skipping {customer['customer_name']} — tab did not open: {e}",
                flush=True
            )
            continue

        customer_meta = extract_customer_header(customer_page)

        opened_notes = open_notes_tab(customer_page)

        if not opened_notes:
            customer_page.close()
            continue

        raw_notes = scrape_jobflo_notes(customer_page)

        days = TIMEFRAME_MAP.get(timeframe, 7)

        relevant_notes = filter_notes_by_timeframe(raw_notes, days)

        if relevant_notes:
            relevant_customers.append({
                "customer_name": customer_meta["customer_name"],
                "project_status": customer_meta["project_status"],
                "notes": relevant_notes
            })

        customer_page.close()

    return relevant_customers
