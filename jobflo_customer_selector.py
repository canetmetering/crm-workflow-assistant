def choose_customers_for_summary(customers):
    if not customers:
        return []

    print("\nRELEVANT JOBFLO CUSTOMERS", flush=True)
    print("-------------------------", flush=True)

    for index, customer in enumerate(customers, start=1):
        print(
            f"{index}. {customer['customer_name']} "
            f"| Status: {customer['project_status']} "
            f"| Relevant Notes: {len(customer['notes'])}",
            flush=True
        )

    selection = input(
        "\nEnter customer numbers (example: 1,3,5) or ALL: "
    ).strip().lower()

    if selection == "all":
        return customers

    try:
        indexes = [
            int(x.strip())
            for x in selection.split(",")
        ]
    except Exception:
        print("Invalid selection.", flush=True)
        return []

    selected = []

    for index in indexes:
        if 1 <= index <= len(customers):
            selected.append(customers[index - 1])

    return selected