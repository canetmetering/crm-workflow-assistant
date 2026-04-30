JOBFLO_CUSTOMERS_URL = "https://app.jobflo.co/customers"


def open_customer_list(page):
    print("Opening JobFlo customer list...", flush=True)

    try:
        page.goto(
            JOBFLO_CUSTOMERS_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Customer list opened.", flush=True)
        return True

    except Exception as error:
        print(f"Failed to open customer list: {error}", flush=True)
        return False