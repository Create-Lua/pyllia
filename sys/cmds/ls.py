__version__ = "1.0"

import os

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    try:
        items = os.listdir(cwd)
        if not items:
            print("Directory is empty.")
            return

        # Optional: mark directories with a slash
        for item in items:
            path = os.path.join(cwd, item)
            if os.path.isdir(path):
                print(f"{item}/")
            else:
                print(item)
    except Exception as e:
        print(f"Error listing directory: {e}")
