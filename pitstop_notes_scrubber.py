from ascentos_notes import scrape_notes
from ai_summarizer import filter_notes_by_timeframe


def pitstop_scrub_notes(project_page, project, timeframe):
    """
    Runs inside PitStop after the project page is opened.
    Scrapes notes immediately, filters by timeframe,
    and tags the project object.

    If zero relevant notes exist, returns None
    so the project gets dropped before customer selection.
    """

    customer_name = project.get("customer_name", "UNKNOWN CUSTOMER")

    print(f"PitStop Notes: scrubbing {customer_name}...")

    raw_notes = scrape_notes(project_page)
    relevant_notes = filter_notes_by_timeframe(
        raw_notes,
        timeframe
    )

    if not relevant_notes:
        print(
            f"PitStop Notes: dropping {customer_name} "
            f"(0 relevant notes)"
        )
        return None

    project["raw_notes"] = raw_notes
    project["relevant_notes"] = relevant_notes

    print(
        f"PitStop Notes: kept {customer_name} "
        f"({len(relevant_notes)} relevant notes)"
    )

    return project