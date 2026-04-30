def choose_projects(projects):
    print("\nCUSTOMERS WITH RELEVANT NOTES", flush=True)
    print("-----------------------------", flush=True)

    for index, project in enumerate(projects, start=1):
        print(
            f"{index}. {project['customer_name']} "
            f"| Project ID: {project['project_id']} "
            f"| Last Updated: {project['last_updated']} "
            f"| Relevant Notes: {len(project.get('relevant_notes', []))}",
            flush=True,
        )

    choice = input(
        "\nEnter customer numbers "
        "(example: 1,3,5) or ALL: "
    ).strip()

    if choice.lower() == "all":
        return projects

    selected = []

    for part in choice.split(","):
        try:
            num = int(part.strip())

            if 1 <= num <= len(projects):
                selected.append(projects[num - 1])

        except Exception:
            pass

    return selected