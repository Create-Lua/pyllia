__version__ = "1.0"

import os

def run(args, shell_state):
    cmds_dir = "cmds"  # your commands folder
    if not os.path.exists(cmds_dir):
        print("No commands folder found.")
        return

    # List all .py files in cmds/ (ignore __init__.py)
    command_files = [f for f in os.listdir(cmds_dir) if f.endswith(".py") and f != "__init__.py"]

    if not command_files:
        print("No commands installed.")
        return

    print("Available commands:")
    for file in command_files:
        command_name = file[:-3]
        print(f"- {command_name}")
