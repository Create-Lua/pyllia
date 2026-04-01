import os

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if len(args) != 2:
        print("Usage: ren <old_name> <new_name>")
        return

    old_name, new_name = args  # handles spaces via quotes
    old_path = os.path.join(cwd, old_name)
    new_path = os.path.join(cwd, new_name)

    if not os.path.exists(old_path):
        print(f"No such file or folder: {old_name}")
        return

    if os.path.exists(new_path):
        print(f"A file or folder already exists with the name: {new_name}")
        return

    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{old_name}' to '{new_name}'")
    except Exception as e:
        print(f"Error renaming: {e}")