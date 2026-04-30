from project_link_parser import extract_project_id_from_href
from pitstop_notes_scrubber import pitstop_scrub_notes


def extract_project_id_from_url(url):
    return extract_project_id_from_href(url)


def run_project_pitstop(registry_page, row, project, timeframe):
    customer_name = project.get("customer_name", "UNKNOWN CUSTOMER")

    print(f"PitStop: opening {customer_name}...")

    project_page = None

    try:
        with registry_page.context.expect_page(timeout=10000) as new_page_info:
            row.click(timeout=5000, force=True)

        project_page = new_page_info.value
        project_page.wait_for_load_state("domcontentloaded", timeout=30000)
        project_page.wait_for_timeout(2500)

        project_url = project_page.url
        project_id = extract_project_id_from_url(project_url)

        if not project_id:
            raise Exception(
                f"Could not extract project ID from URL: {project_url}"
            )

        project["project_id"] = project_id
        project["project_href"] = project_url

        print(f"PitStop: {customer_name} tagged with Project ID {project_id}")

        return pitstop_scrub_notes(
            project_page,
            project,
            timeframe
        )

    finally:
        if project_page:
            try:
                project_page.close()
            except Exception:
                pass