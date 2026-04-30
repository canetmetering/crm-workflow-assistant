def wait_for_jobflo_login():
    while True:
        answer = input(
            "\nManually sign into JobFlo in the remote browser. "
            "Are you logged in and ready to continue? (y/n): "
        ).strip().lower()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no"]:
            print("Waiting. Finish logging in, then answer y.", flush=True)
            continue

        print("Please enter y or n.", flush=True)