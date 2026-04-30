from project_list_page_scanner import scan_visible_project_rows
from project_list_pagination import go_to_next_project_list_page


def scan_all_project_pages_for_updates(list_page, timeframe, max_pages=100):
    all_projects = []
    seen_project_ids = set()
    page_number = 1

    while page_number <= max_pages:
        print(f"\nScanning registry page {page_number}...")

        matched_projects = scan_visible_project_rows(
            list_page,
            timeframe
        )

        for project in matched_projects:
            customer_name = project.get("customer_name")

            if not customer_name:
                continue

            if customer_name not in seen_project_ids:
                seen_project_ids.add(customer_name)
                all_projects.append(project)

        if not go_to_next_project_list_page(list_page):
            break

        page_number += 1

    print(f"\nTotal matched projects: {len(all_projects)}")

    for index, project in enumerate(all_projects, start=1):
        print(
            f"{index}. {project['customer_name']} "
            f"| Last Updated: {project['last_updated']}"
        )

    return all_projects
