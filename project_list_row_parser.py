from project_last_updated_parser import (
    extract_last_updated_marker,
    last_updated_is_in_timeframe,
)


BLOCKED_EXACT_LINES = {
    "ACTIVE",
    "CANCELED",
    "CANCELLED",
    "COMPLETED",
    "NRG",
    "PROJECT NAME",
    "ADDRESS",
    "SALES TEAM",
    "PROJECT STATUS",
    "ACTIVE STAGES",
    "TAGS",
    "ACTIVE ISSUES",
    "LAST UPDATED",
}


def clean_customer_name(line):
    line = line.strip()

    for i, char in enumerate(line):
        if char.isdigit():
            return line[:i].strip()

    return line


def extract_customer_name(row_text):
    lines = [line.strip() for line in row_text.split("\n") if line.strip()]

    for line in lines:
        if line.upper() in BLOCKED_EXACT_LINES:
            continue

        cleaned = clean_customer_name(line)

        if len(cleaned.split()) >= 2:
            return cleaned

    return "UNKNOWN CUSTOMER"


def parse_project_list_row(row, timeframe):
    row_text = row.inner_text()

    if not row_text:
        return None

    marker = extract_last_updated_marker(row_text)

    if not marker:
        return None

    if not last_updated_is_in_timeframe(marker, timeframe):
        return None

    customer_name = extract_customer_name(row_text)

    return {
        "customer_name": customer_name,
        "last_updated": marker,
        "row_text": row_text,
    }