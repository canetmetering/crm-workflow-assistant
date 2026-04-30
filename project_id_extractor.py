from click_project_row import click_project_row
from click_project_hamburger import click_project_hamburger
from click_project_details import click_project_details


def attach_project_id(registry_page, project):
    project_page = None

    try:
        project_page = click_project_row(registry_page, project)
        click_project_hamburger(project_page)
        project_id = click_project_details(project_page)

        project["project_id"] = project_id
        return project

    finally:
        try:
            if project_page and project_page != registry_page:
                project_page.close()
                registry_page.bring_to_front()
                registry_page.wait_for_timeout(1000)
        except Exception:
            pass


def attach_project_ids_to_projects(registry_page, projects):
    updated_projects = []

    for project in projects:
        customer_name = project.get("customer_name", "UNKNOWN CUSTOMER")
        updated = attach_project_id(registry_page, project)
        updated_projects.append(updated)

    return updated_projects