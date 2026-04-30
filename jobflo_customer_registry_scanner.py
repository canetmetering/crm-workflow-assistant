import time


JENNY_FU_STOP_NAME = "Jenny Fu"


def get_customer_rows(page):
    selectors = [
        "tbody tr",
        "table tbody tr",
        "[role='row']",
        ".MuiDataGrid-row"
    ]

    for selector in selectors:
        rows = page.locator(selector)

        if rows.count() > 1:
            return rows

    return page.locator("tbody tr")


def wait_for_customer_table(page):
    print("Waiting for customer table...", flush=True)

    for _ in range(20):
        rows = get_customer_rows(page)

        if rows.count() > 1:
            return rows

        time.sleep(1)

    return get_customer_rows(page)


def extract_customer_from_row(row):
    cells = row.locator("td")

    if cells.count() < 2:
        return None

    customer_id = cells.nth(0).inner_text().strip()
    customer_name = cells.nth(1).inner_text().strip()

    if not customer_id or not customer_name:
        return None

    return {
        "customer_id": customer_id,
        "customer_name": customer_name
    }


def scan_jobflo_customers_until_jenny(page):
    print("Scanning JobFlo customer list...", flush=True)

    rows = wait_for_customer_table(page)
    row_count = rows.count()

    print(f"Visible customer rows found: {row_count}", flush=True)

    customers = []

    for i in range(row_count):
        row = rows.nth(i)
        customer = extract_customer_from_row(row)

        if not customer:
            continue

        print(f"Found: {customer['customer_name']}", flush=True)
        customers.append(customer)

        if customer["customer_name"].strip().lower() == JENNY_FU_STOP_NAME.lower():
            print("Reached Jenny Fu. Hard stop.", flush=True)
            break

    print(f"Total customers to scrub: {len(customers)}", flush=True)
    return customers, True
