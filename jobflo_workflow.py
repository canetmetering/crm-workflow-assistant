from workflow_selector import choose_workflow
from jobflo_open_customer_list import open_customer_list
from jobflo_customer_registry_scanner import scan_jobflo_customers_until_jenny
from jobflo_scrubber import scrub_jobflo_customers
from jobflo_customer_selector import choose_customers_for_summary
from jobflo_summarizer import summarize_jobflo_customers
from jobflo_report_exporter import export_jobflo_report


def run_jobflo_workflow(context, timeframe=None, timeframe_label=None):
    print("Starting JobFlo workflow...", flush=True)
    print("\nJobFlo Workflow", flush=True)
    print("---------------", flush=True)

    if not timeframe:
        timeframe, timeframe_label = choose_workflow()

    if not timeframe:
        return

    registry_page = context.pages[0]

    print("Opening JobFlo customer list...", flush=True)

    if not open_customer_list(registry_page):
        print("Failed to open customer list.", flush=True)
        return

    print("Customer list opened.", flush=True)

    customers, _ = scan_jobflo_customers_until_jenny(registry_page)

    if not customers:
        print("No customers found.", flush=True)
        return

    relevant_customers = scrub_jobflo_customers(
        context,
        customers,
        timeframe
    )

    if not relevant_customers:
        print("No customers with relevant notes found.", flush=True)
        return

    selected_customers = choose_customers_for_summary(relevant_customers)

    if not selected_customers:
        print("No customers selected.", flush=True)
        return

    print("Generating summaries...", flush=True)

    summaries = summarize_jobflo_customers(
        selected_customers,
        timeframe_label
    )

    report_file = export_jobflo_report(
        summaries,
        timeframe_label
    )

    print(f"\nDownloadable report created: {report_file}", flush=True)

    print("\nJOBFLO REPORT", flush=True)
    print("-------------", flush=True)

    for item in summaries:
        print(f"\n{item['customer_name']} | {item['project_status']}", flush=True)
        print(item["summary"], flush=True)
        print("\n---", flush=True)
