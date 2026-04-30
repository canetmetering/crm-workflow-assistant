def choose_platform():
    print("\nChoose CRM Platform", flush=True)
    print("-------------------", flush=True)
    print("A = AscentOS", flush=True)
    print("J = JobFlo", flush=True)

    choice = input("\nChoose platform: ").strip().lower()

    if choice == "a":
        return "ascent"

    if choice == "j":
        return "jobflo"

    print("Invalid platform choice.", flush=True)
    return None