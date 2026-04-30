import re


def extract_project_id_from_href(href):
    if not href:
        return None

    match = re.search(
        r"/projects/(\d{5})(?:\?|/|$)",
        href
    )

    if match:
        return match.group(1)

    return None


def extract_project_link_info(row):
    """
    Search the entire row for ANY element containing
    an href that points to /projects/#####.
    """

    elements = row.locator("[href]")
    count = elements.count()

    for i in range(count):
        try:
            element = elements.nth(i)
            href = element.get_attribute("href")

            if not href:
                continue

            project_id = extract_project_id_from_href(href)

            if project_id:
                try:
                    link_text = element.inner_text().strip()
                except Exception:
                    link_text = None

                return {
                    "project_id": project_id,
                    "project_href": href,
                    "link_text": link_text,
                }

        except Exception:
            pass

    return {
        "project_id": None,
        "project_href": None,
        "link_text": None,
    }