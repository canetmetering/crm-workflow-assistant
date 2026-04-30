JOBFLO_CUSTOMER_EDIT_BASE_URL = "https://app.jobflo.co/customers/edit"


def open_customer_in_new_tab(customer, page):
    customer_id = customer["customer_id"]

    customer_url = (
        f"{JOBFLO_CUSTOMER_EDIT_BASE_URL}/"
        f"{customer_id}"
    )

    print(
        f"Opening customer in new tab: {customer_url}",
        flush=True
    )

    page.evaluate(
        f'window.open("{customer_url}", "_blank");'
    )
