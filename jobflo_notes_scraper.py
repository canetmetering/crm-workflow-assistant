import re
from datetime import datetime, timedelta


NOTES_JUNK = {
    "Reply", "Notes", "Files", "Milestones",
    "Proposals", "Contracts", "Production",
    "Create Note", "@groups", "Pinned",
    "All Notes", "Unresolved", "Operations",
    "Sales", "Customer", "Load more...",
}


def parse_note_datetime(date_string):
    date_string = date_string.strip()

    for fmt in ["%m/%d/%Y %I:%M%p", "%m/%d/%Y %I:%M %p"]:
        try:
            return datetime.strptime(date_string, fmt)
        except Exception:
            pass

    return None


def load_all_notes(page, max_loads=3):
    print("Loading all notes...", flush=True)

    for attempt in range(max_loads):
        try:
            load_more = page.locator("text=Load more...")

            if load_more.count() == 0:
                print(f"No more notes to load after {attempt} loads.", flush=True)
                break

            load_more.first.scroll_into_view_if_needed(timeout=3000)
            load_more.first.click(timeout=5000)
            page.wait_for_timeout(2000)
            print(f"Loaded more notes ({attempt + 1}).", flush=True)

        except Exception:
            print(f"No more notes to load after {attempt} loads.", flush=True)
            break


def scrape_jobflo_notes(page):
    print("Scraping JobFlo notes...", flush=True)

    load_all_notes(page, max_loads=3)
    page.wait_for_timeout(1000)

    note_blocks = []

    try:
        body_text = page.locator("body").inner_text()
        lines = [l.strip() for l in body_text.split("\n") if l.strip()]

        current_note = None

        for line in lines:
            parsed_dt = parse_note_datetime(line)

            if not parsed_dt:
                match = re.search(
                    r"\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s*[APap][Mm]",
                    line
                )
                if match:
                    parsed_dt = parse_note_datetime(match.group(0).strip())

            if parsed_dt:
                if current_note:
                    note_blocks.append(current_note)

                current_note = {
                    "timestamp": line,
                    "parsed_dt": parsed_dt,
                    "content": "",
                }

            elif current_note:
                if line not in NOTES_JUNK:
                    current_note["content"] += line + " "

        if current_note:
            note_blocks.append(current_note)

    except Exception as e:
        print(f"Error scraping notes: {e}", flush=True)

    print(f"Raw note blocks found: {len(note_blocks)}", flush=True)
    return note_blocks


def filter_notes_by_timeframe(notes, timeframe_days):
    relevant = []
    cutoff = datetime.now() - timedelta(days=timeframe_days)

    for note in notes:
        parsed_dt = note.get("parsed_dt")

        if not parsed_dt:
            continue

        if parsed_dt >= cutoff:
            relevant.append({
                "timestamp": note.get("timestamp", ""),
                "content": note.get("content", "").strip(),
            })

    print(f"Relevant JobFlo notes found: {len(relevant)}", flush=True)
    return relevant
