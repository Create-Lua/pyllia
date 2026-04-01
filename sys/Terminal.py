__version__ = "1.0"

import os
import importlib.util
import sys
import shlex
import json

# ----------------------------
# Shell State
# ----------------------------
current_dir = os.getcwd()  # Internal shell directory
cmds_dir = os.path.join(os.getcwd(), "cmds")  # folder where command modules live
commands = {}  # cache of loaded modules

# ----------------------------
# Ensure config folder exists
# ----------------------------
config_folder = os.path.join(os.getcwd(), "config")
if not os.path.exists(config_folder):
    os.mkdir(config_folder)

config_path = os.path.join(config_folder, "config.json")

# Create default config if missing
if not os.path.exists(config_path):
    default_config = {
        "prompt_color": "green",
        "path_style": "short",
        "show_username": True
    }
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=2)

# ----------------------------
# Load a command dynamically
# ----------------------------
def load_command(cmd_name):
    cmd_path = os.path.join(cmds_dir, f"{cmd_name}.py")
    if not os.path.exists(cmd_path):
        return None

    spec = importlib.util.spec_from_file_location(cmd_name, cmd_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[cmd_name] = module
    spec.loader.exec_module(module)
    return module

# ----------------------------
# Shell prompt (live config)
# ----------------------------
import os
import json
import getpass

import os
import json
import getpass

def get_prompt(shell_state):
    # Reload config each time
    config_folder = os.path.join(os.getcwd(), "config")
    config_path = os.path.join(config_folder, "config.json")

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                current_config = json.load(f)
        except Exception:
            current_config = {}
    else:
        current_config = {}

    # Defaults
    prompt_color = current_config.get("prompt_color", "green")
    path_style = current_config.get("path_style", "short")
    show_username = current_config.get("show_username", True)

    # Current directory
    cwd = shell_state.get("current_dir", os.getcwd())

    if path_style == "long":
        display_path = cwd
    else:  # short
        display_path = os.path.basename(cwd) or "/"

    # Username
    try:
        username = getpass.getuser()
    except Exception:
        username = "user"

    # Build prompt
    if show_username:
        prompt_str = f"{username}@{display_path} > "
    else:
        prompt_str = f"{display_path} > "

    # Colors
    color_codes = {
        "green": "\033[92m",
        "blue": "\033[94m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "reset": "\033[0m"
    }
    color = color_codes.get(prompt_color, "\033[92m")

    return f"{color}{prompt_str}{color_codes['reset']}"

def prompt(shell_state):
    return input(get_prompt(shell_state)).strip()

# ----------------------------
# Main shell loop
# ----------------------------
def shell():
    shell_state = {"current_dir": os.getcwd()}

    while True:
        userinput = prompt(shell_state)
        if not userinput:
            continue

        parts = shlex.split(userinput)
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name.lower() == "exit":
            print("Exiting shell...")
            break

        if cmd_name not in commands:
            module = load_command(cmd_name)
            if module:
                commands[cmd_name] = module
            else:
                print(f"Unknown command: {cmd_name}")
                continue

        try:
            commands[cmd_name].run(args, shell_state)
        except Exception as e:
            print(f"Error running {cmd_name}: {e}")

# ----------------------------
# Run shell
# ----------------------------
if __name__ == "__main__":
    shell()
