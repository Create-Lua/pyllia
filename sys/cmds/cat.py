__version__ = "1.0"

import os

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if not args:
        print("Usage: cat <filename>")
        return

    file_name = args[0]  # now handles spaces via quotes
    file_path = os.path.join(cwd, file_name)

    if not os.path.exists(file_path):
        print(f"No such file: {file_name}")
        return

    if os.path.isdir(file_path):
        print(f"{file_name} is a directory")
        return

    try:
        with open(file_path, "r") as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
