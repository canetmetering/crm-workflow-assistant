from browser_tab_manager import open_registry_clean
from workflow_selector import choose_workflow
from project_selector import choose_projects
from ascentos_project_list_updates import scan_all_project_pages_for_updates
from recent_update_summarizer import summarize_recent_updates
from report_exporter import export_report


ASCENT_REGISTRY_URL = "https://app.ascentos.ai/project-types/2/projects"


def run_ascent_workflow(context, timeframe=None, timeframe_label=None):
    print("Opening AscentOS project registry...", flush=True)

    page = open_registry_clean(
        context,
        ASCENT_REGISTRY_URL
    )

    if not timeframe:
        timeframe, timeframe_label = choose_workflow()

    if not timeframe:
        print("Workflow cancelled.", flush=True)
        return

    print(f"Scanning AscentOS projects for timeframe: {timeframe_label}", flush=True)

    projects = scan_all_project_pages_for_updates(
        page,
        timeframe
    )

    if not projects:
        print("No relevant AscentOS projects found.", flush=True)
        return

    selected_projects = choose_projects(projects)

    if not selected_projects:
        print("No projects selected.", flush=True)
        return

    print("Generating summaries...", flush=True)

    summaries = summarize_recent_updates(
        selected_projects,
        timeframe_label
    )

    report_file = export_report(
        summaries,
        timeframe_label
    )

    print(f"\nDownloadable report created: {report_file}", flush=True)

    print("\nRECENT UPDATE SUMMARIES", flush=True)
    print("-----------------------", flush=True)

    for item in summaries:
        print(f"\n{item['customer_name']}", flush=True)
        print(item["summary"], flush=True)
        print("\n---", flush=True)
