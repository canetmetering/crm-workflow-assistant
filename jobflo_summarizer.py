from openai import OpenAI

client = OpenAI()

MODEL = "gpt-5.4-mini"


def format_jobflo_notes(notes):
    if not notes:
        return ""

    formatted = []

    for note in notes:
        timestamp = note.get("timestamp", "UNKNOWN DATE")
        content = note.get("content", "").strip()

        if content:
            formatted.append(f"{timestamp}\n{content}")

    return "\n\n---\n\n".join(formatted)


def summarize_jobflo_customer(customer, timeframe_label):
    customer_name = customer.get("customer_name", "UNKNOWN CUSTOMER")
    project_status = customer.get("project_status", "UNKNOWN STATUS")
    notes = customer.get("notes", [])

    notes_text = format_jobflo_notes(notes)

    if not notes_text:
        return {
            "customer_name": customer_name,
            "project_status": project_status,
            "summary": "No relevant notes found in the selected timeframe.",
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
Project Status: {project_status}

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

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "customer_name": customer_name,
        "project_status": project_status,
        "summary": response.choices[0].message.content,
    }


def summarize_jobflo_customers(customers, timeframe_label):
    summaries = []

    for customer in customers:
        summaries.append(
            summarize_jobflo_customer(customer, timeframe_label)
        )

    return summaries
