import re
from datetime import datetime, timedelta


DATE_HEADER_PATTERN = re.compile(
    r"^\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$",
    re.IGNORECASE,
)

FULL_TIMESTAMP_PATTERN = re.compile(
    r"^\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}\s*(AM|PM)$",
    re.IGNORECASE,
)

WEEKDAY_TIME_PATTERN = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+\d{1,2}:\d{2}\s*(AM|PM)$",
    re.IGNORECASE,
)

TIME_ONLY_PATTERN = re.compile(
    r"^\d{1,2}:\d{2}\s*(AM|PM)$",
    re.IGNORECASE,
)


def get_cutoff_datetime(timeframe):
    now = datetime.now()

    if timeframe == "48h":
        return now - timedelta(hours=48)

    if timeframe == "week":
        return now - timedelta(days=7)

    return now - timedelta(days=3650)


def is_date_header(line):
    return bool(DATE_HEADER_PATTERN.match(line.strip()))


def is_full_timestamp(line):
    return bool(FULL_TIMESTAMP_PATTERN.match(line.strip()))


def is_weekday_time(line):
    return bool(WEEKDAY_TIME_PATTERN.match(line.strip()))


def is_time_only(line):
    return bool(TIME_ONLY_PATTERN.match(line.strip()))


def parse_date_header(line):
    now = datetime.now()

    try:
        parsed = datetime.strptime(line.strip(), "%d %b")
        return parsed.replace(year=now.year)
    except Exception:
        return None


def parse_full_timestamp(line):
    line = line.strip()

    for fmt in ["%m/%d/%Y %I:%M %p", "%m/%d/%y %I:%M %p"]:
        try:
            return datetime.strptime(line, fmt)
        except Exception:
            pass

    return None


def parse_weekday_time(line, current_date_header=None):
    line = line.strip()

    match = WEEKDAY_TIME_PATTERN.match(line)

    if not match:
        return None

    time_part = re.sub(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+",
        "",
        line,
        flags=re.IGNORECASE,
    )

    try:
        parsed_time = datetime.strptime(time_part, "%I:%M %p")
    except Exception:
        return None

    if current_date_header:
        return current_date_header.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0,
        )

    return None


def parse_time_only(line, current_date_header=None):
    line = line.strip()

    try:
        parsed_time = datetime.strptime(line, "%I:%M %p")
    except Exception:
        return None

    if current_date_header:
        return current_date_header.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0,
        )

    return None


def parse_note_timestamp(line, current_date_header=None):
    if is_full_timestamp(line):
        return parse_full_timestamp(line)

    if is_weekday_time(line):
        return parse_weekday_time(line, current_date_header)

    if is_time_only(line):
        return parse_time_only(line, current_date_header)

    return None


def note_is_within_timeframe(parsed_datetime, timeframe):
    if not parsed_datetime:
        return False

    return parsed_datetime >= get_cutoff_datetime(timeframe)
