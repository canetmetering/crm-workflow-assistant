from note_date_parser import (
    is_date_header,
    parse_date_header,
    parse_note_timestamp,
    note_is_within_timeframe,
)


def split_note_blocks(raw_notes):
    lines = [line.strip() for line in raw_notes.split("\n") if line.strip()]

    note_blocks = []
    current_date_header = None
    current_block = None

    for line in lines:
        if is_date_header(line):
            current_date_header = parse_date_header(line)
            continue

        parsed_timestamp = parse_note_timestamp(line, current_date_header)

        if parsed_timestamp:
            if current_block:
                note_blocks.append(current_block)

            current_block = {
                "timestamp": line,
                "parsed_datetime": parsed_timestamp,
                "content": "",
            }
            continue

        if current_block:
            current_block["content"] += line + "\n"

    if current_block:
        note_blocks.append(current_block)

    return note_blocks


def filter_notes_by_timeframe(raw_notes, timeframe):
    note_blocks = split_note_blocks(raw_notes)

    relevant_notes = []

    for block in note_blocks:
        if note_is_within_timeframe(block["parsed_datetime"], timeframe):
            relevant_notes.append({
                "timestamp": block["timestamp"],
                "content": block["content"].strip(),
            })

    print(f"Relevant note blocks found: {len(relevant_notes)}")

    return relevant_notes