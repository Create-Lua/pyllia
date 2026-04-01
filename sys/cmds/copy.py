import os
import shutil

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if len(args) != 2:
        print("Usage: copy <source> <destination>")
        return

    src_name, dest_name = args
    src_path = os.path.join(cwd, src_name)
    dest_path = os.path.join(cwd, dest_name)

    if not os.path.exists(src_path):
        print(f"No such file or folder: {src_name}")
        return

    if os.path.exists(dest_path):
        print(f"A file or folder already exists with the name: {dest_name}")
        return

    try:
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"File copied: {src_name} → {dest_name}")
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
            print(f"Folder copied: {src_name} → {dest_name}")
    except Exception as e:
        print(f"Error copying: {e}")