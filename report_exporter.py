from datetime import datetime
from pathlib import Path


REPORT_DIR = Path("reports")


def export_report(summaries, timeframe_label=""):
    REPORT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = REPORT_DIR / f"ascent_report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("ASCENTOS RECENT UPDATE REPORT\n")
        file.write("=" * 40)
        file.write("\n")

        if timeframe_label:
            file.write(f"Timeframe: {timeframe_label}\n")

        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n")
        file.write("=" * 40)
        file.write("\n\n")

        for index, item in enumerate(summaries, start=1):
            customer_name = item.get("customer_name", "UNKNOWN CUSTOMER")
            project_id = item.get("project_id", "UNKNOWN PROJECT")
            project_url = item.get("project_url", "")
            summary = item.get("summary", "NO SUMMARY AVAILABLE")

            file.write(f"{index}. {customer_name}\n")
            file.write(f"Project ID: {project_id}\n")

            if project_url:
                file.write(f"Project URL: {project_url}\n")

            file.write("-" * 40)
            file.write("\n")
            file.write(summary)
            file.write("\n\n")

    print(f"\nReport exported: {filename}", flush=True)

    return str(filename)