from openai import OpenAI

client = OpenAI()

MODEL = "gpt-5.4-mini"


def format_relevant_notes(relevant_notes):
    if not relevant_notes:
        return ""

    formatted = []

    for note in relevant_notes:
        timestamp = note.get("timestamp", "UNKNOWN DATE")
        content = note.get("content", "").strip()

        if content:
            formatted.append(f"{timestamp}\n{content}")

    return "\n\n---\n\n".join(formatted)


def summarize_recent_update(project, timeframe_label):
    customer_name = project.get("customer_name", "UNKNOWN CUSTOMER")
    project_id = project.get("project_id", "UNKNOWN PROJECT")
    project_url = project.get("project_url", "")
    relevant_notes = project.get("relevant_notes", [])

    notes_text = format_relevant_notes(relevant_notes)

    if not notes_text:
        return {
            "project_id": project_id,
            "customer_name": customer_name,
            "project_url": project_url,
            "summary": "No relevant timestamped notes found in the selected timeframe.",
        }

    prompt = f"""
You are a solar operations assistant.

Summarize ONLY the timestamped notes provided below.
The selected timeframe is: {timeframe_label}.

Rules:
- Short, snappy bullet points.
- Separate big rocks from little rocks.
- Report facts only.
- No value judgments.
- No generic filler.
- Do not mention CRM junk or UI text.
- Do not summarize anything outside the provided timestamped notes.
- Focus on what changed, blockers, customer/admin follow-up, and next action.

Customer: {customer_name}
Project ID: {project_id}
Project URL: {project_url}

Relevant Timestamped Notes:
{notes_text}

Return exactly this format:

Big Rocks:
- <major update>
- <major blocker/milestone if any>

Little Rocks:
- <minor/admin detail if any>

Next Action:
- <specific next action based only on notes>

Risk / Blocker:
- <specific blocker, or "None identified in recent notes">
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    return {
        "project_id": project_id,
        "customer_name": customer_name,
        "project_url": project_url,
        "summary": response.output_text,
    }


def summarize_recent_updates(project_results, timeframe_label):
    summaries = []

    for project in project_results:
        summaries.append(summarize_recent_update(project, timeframe_label))

    return summaries