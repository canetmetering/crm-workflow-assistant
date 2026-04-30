PIPELINE_JUNK = {
    "9+", "Back To All Customers", "Dashboard", "Leads",
    "Customers", "Calendar", "PROGRESS TRACKER",
}


def extract_customer_header(page):
    customer_name = ""
    project_status = ""

    try:
        page.wait_for_timeout(2000)
    except Exception:
        pass

    try:
        body_text = page.locator("body").inner_text()
        lines = [l.strip() for l in body_text.split("\n") if l.strip()]

        for i, line in enumerate(lines):
            if line == "CUSTOMER" and i + 1 < len(lines):
                customer_name = lines[i + 1].strip()
                break

        for i, line in enumerate(lines):
            if line == "PROGRESS TRACKER":
                pipeline = []
                for j in range(max(0, i - 10), i):
                    candidate = lines[j].strip()
                    if (
                        candidate
                        and candidate not in PIPELINE_JUNK
                        and len(candidate) > 2
                        and len(candidate) < 60
                    ):
                        pipeline.append(candidate)

                if pipeline:
                    if pipeline[-1] == "Clean Deal" and len(pipeline) >= 2:
                        project_status = pipeline[-2]
                    else:
                        project_status = pipeline[-1]
                break

    except Exception as e:
        print(f"Header extraction error: {e}", flush=True)

    print(
        f"Customer: {customer_name or 'NOT FOUND'} | "
        f"Status: {project_status or 'NOT FOUND'}",
        flush=True
    )

    return {
        "customer_name": customer_name,
        "project_status": project_status,
    }
