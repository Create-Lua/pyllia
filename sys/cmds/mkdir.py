import os

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if not args:
        print("Usage: mkdir <folder_name>")
        return

    folder_name = args[0]  # handles spaces via quotes
    new_path = os.path.join(cwd, folder_name)

    try:
        if os.path.exists(new_path):
            print(f"Folder already exists: {folder_name}")
            return

        os.mkdir(new_path)
        print(f"Folder created: {folder_name}")
    except Exception as e:
        print(f"Error creating folder: {e}")