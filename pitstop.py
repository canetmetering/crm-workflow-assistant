from playwright.sync_api import Error as PlaywrightError

from browser_recovery import recover_registry_page
from pitstop_project_runner import run_project_pitstop


def pitstop_process_project(registry_page, row, project, timeframe):
    customer_name = project.get("customer_name", "UNKNOWN CUSTOMER")

    try:
        return run_project_pitstop(
            registry_page,
            row,
            project,
            timeframe
        )

    except PlaywrightError as e:
        print(f"PitStop browser issue for {customer_name}: {e}")
        print("Attempting browser recovery and one retry...")

        recover_registry_page(registry_page)

        try:
            return run_project_pitstop(
                registry_page,
                row,
                project,
                timeframe
            )

        except Exception as retry_error:
            print(
                f"PitStop retry failed for {customer_name}: "
                f"{retry_error}"
            )
            return None

    except Exception as e:
        print(f"PitStop failed for {customer_name}: {e}")
        return None