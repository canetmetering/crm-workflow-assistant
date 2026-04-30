def choose_workflow():
    print("\nWorkflow Timeframe", flush=True)
    print("------------------", flush=True)
    print("1 = Last 48 hours", flush=True)
    print("2 = Last week", flush=True)
    print("3 = Full project summaries", flush=True)

    choice = input("\nChoose workflow: ").strip()

    if choice == "1":
        return "48h", "last 48 hours"

    if choice == "2":
        return "week", "last week"

    if choice == "3":
        print("Full project summaries coming next.", flush=True)
        return None, None

    print("Invalid choice.", flush=True)
    return None, None
