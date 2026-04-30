from project_list_row_parser import parse_project_list_row
from pitstop import pitstop_process_project


def scan_visible_project_rows(list_page, timeframe):
    rows = list_page.locator("tbody tr")
    row_count = rows.count()

    matched_projects = []

    print(f"Visible registry rows found: {row_count}")

    for i in range(row_count):
        try:
            row = rows.nth(i)

            project = parse_project_list_row(
                row,
                timeframe
            )

            if not project:
                continue

            print(
                f"MATCHED: {project['customer_name']} "
                f"| Last Updated: {project['last_updated']}"
            )

            project = pitstop_process_project(
                list_page,
                row,
                project,
                timeframe
            )

            if project:
                matched_projects.append(project)

        except Exception as e:
            print(f"Skipped row {i}: {e}")

    print(
        f"Matched note-bearing projects on this page: "
        f"{len(matched_projects)}"
    )

    return matched_projects