from datetime import datetime, timedelta
import re


WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def extract_last_updated_marker(text):
    if not text:
        return None

    patterns = [
        r"\bAbout\s+\d+\s+hours?\s+ago\b",
        r"\b\d+\s+hours?\s+ago\b",
        r"\b\d+\s+minutes?\s+ago\b",
        r"\bjust now\b",
        r"\bMonday\b|\bTuesday\b|\bWednesday\b|\bThursday\b|\bFriday\b|\bSaturday\b|\bSunday\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            return match.group(0)

    return None


def parse_last_updated(marker):
    if not marker:
        return None

    now = datetime.now()
    marker = marker.strip()
    lower = marker.lower()

    if "just now" in lower:
        return now.date()

    if "hour" in lower or "minute" in lower:
        return now.date()

    if lower in WEEKDAYS:
        days_back = (now.weekday() - WEEKDAYS[lower]) % 7
        return (now - timedelta(days=days_back)).date()

    for fmt in ["%m/%d/%Y", "%m/%d/%y"]:
        try:
            return datetime.strptime(marker, fmt).date()
        except Exception:
            pass

    try:
        parsed = datetime.strptime(marker, "%d %b")
        return parsed.replace(year=now.year).date()
    except Exception:
        pass

    return None


def last_updated_is_in_timeframe(marker, timeframe):
    parsed_date = parse_last_updated(marker)

    if not parsed_date:
        return False

    today = datetime.now().date()

    if timeframe == "48h":
        return parsed_date >= today - timedelta(days=2)

    if timeframe == "week":
        return parsed_date >= today - timedelta(days=7)

    return True