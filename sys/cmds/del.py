import os
import shutil

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if not args:
        print("Usage: del <file_or_folder_name>")
        return

    target_name = args[0]  # handles spaces via quotes
    target_path = os.path.join(cwd, target_name)

    if not os.path.exists(target_path):
        print(f"No such file or folder: {target_name}")
        return

    try:
        if os.path.isfile(target_path):
            os.remove(target_path)
            print(f"File deleted: {target_name}")
        elif os.path.isdir(target_path):
            if not os.listdir(target_path):
                os.rmdir(target_path)
                print(f"Folder deleted: {target_name}")
            else:
                confirm = input(f"Folder not empty. Delete all contents of '{target_name}'? (y/n): ")
                if confirm.lower() == "y":
                    shutil.rmtree(target_path)
                    print(f"Folder deleted: {target_name}")
                else:
                    print("Deletion canceled.")
    except Exception as e:
        print(f"Error deleting {target_name}: {e}")