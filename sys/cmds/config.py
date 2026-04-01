__version__ = "1.0"

import os
import json

ALLOWED_VALUES = {
    "prompt_color": ["green", "blue", "red", "yellow"],
    "path_style": ["short", "long"],
    "show_username": [True, False]
}

def run(args, shell_state):
    """
    Usage:
      config -r                # reload config
      config <option> <value>  # set option (only allowed values)
    """
    config_folder = os.path.join(os.getcwd(), "config")
    config_path = os.path.join(config_folder, "config.json")

    if not os.path.exists(config_folder):
        os.mkdir(config_folder)

    # Load existing config
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except Exception:
            config = {}
    else:
        config = {}

    # Handle reload flag
    if args and args[0] == "-r":
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                print("Config reloaded successfully.")
            except Exception as e:
                print(f"Failed to reload config: {e}")
        else:
            print("Config file not found.")
        return

    # Handle setting option
    if len(args) >= 2:
        option = args[0]
        value = args[1]

        # Convert to proper type
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

        # Check if option is allowed and value is valid
        if option not in ALLOWED_VALUES:
            print(f"Invalid option: {option}")
            return

        if value not in ALLOWED_VALUES[option]:
            print(f"Invalid value for {option}. Allowed: {ALLOWED_VALUES[option]}")
            return

        # Save config
        config[option] = value
        try:
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            print(f"{option} set to {value}")
        except Exception as e:
            print(f"Failed to save config: {e}")
        return

    print("Usage:\n  config -r               # reload config\n  config <option> <value>  # set option")
