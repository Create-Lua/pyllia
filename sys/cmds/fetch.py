__version__ = "1.0"

import os
import json
import urllib.request

# ----------------------------
# Repo settings
# ----------------------------
repo_user = "Create-Lua"
repo_name = "pyllia"

# ----------------------------
# Helper functions
# ----------------------------
def raw_url(branch, filepath):
    """Return raw GitHub URL for a file"""
    return f"https://raw.githubusercontent.com/{repo_user}/{repo_name}/{branch}/{filepath}"

def download_file(url, dest_path):
    """Download a file and return True if successful, False otherwise"""
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception:
        return False

# ----------------------------
# Main fetch command
# ----------------------------
def run(args, shell_state):
    if len(args) < 1:
        print("Usage: fetch -S|-R|-U|-Ua <package_name>")
        return

    flag = args[0]
    current_dir = shell_state["current_dir"]
    cmds_dir = os.path.join(current_dir, "cmds")
    config_dir = os.path.join(current_dir, "config")
    terminal_path = os.path.join(current_dir, "Terminal.py")

    os.makedirs(cmds_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

    installed_packages = [
        f for f in os.listdir(cmds_dir)
        if f.endswith(".py") and f != "fetch.py"
    ]

    # ------------------- INSTALL -------------------
    if flag == "-S":
        if len(args) < 2:
            print("Usage: fetch -S <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        url = raw_url("main", f"cmds/{package}.py")
        if download_file(url, dest_path):
            print(f"{package} Installed/Updated successfully")
        else:
            print("Package not found")

    # ------------------- REMOVE -------------------
    elif flag == "-R":
        if len(args) < 2:
            print("Usage: fetch -R <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
                print(f"{package} removed successfully")
            except Exception as e:
                print(f"Failed to remove {package}: {e}")
        else:
            print(f"No such package installed: {package}")

    # ------------------- UPDATE -------------------
    elif flag == "-U":
        updated_any = False
        for pkg_file in installed_packages:
            local_path = os.path.join(cmds_dir, pkg_file)
            url = raw_url("main", f"cmds/{pkg_file}")
            if download_file(url, local_path):
                print(f"{pkg_file[:-3]} Updated successfully")
                updated_any = True
        if not updated_any:
            print("All packages up to date")

    # ------------------- UPDATE + SYS -------------------
    elif flag == "-Ua":
        updated_any = False

        # Step 1: Fetch sys commands list
        sys_cmds_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/contents/sys/cmds"
        try:
            with urllib.request.urlopen(sys_cmds_url) as response:
                data = json.load(response)
            sys_files = [f["name"] for f in data if f["name"].endswith(".py")]
        except Exception:
            sys_files = []

        # Step 2: Update sys commands
        for cmd_file in sys_files:
            dest_path = os.path.join(cmds_dir, cmd_file)
            if download_file(raw_url("sys", f"sys/cmds/{cmd_file}"), dest_path):
                print(f"{cmd_file[:-3]} Updated successfully")
                updated_any = True

        # Step 3: Terminal.py
        if download_file(raw_url("sys", "sys/Terminal.py"), terminal_path):
            print("Terminal.py Updated successfully")
            updated_any = True

        # Step 4: config.json
        config_path = os.path.join(config_dir, "config.json")
        try:
            with urllib.request.urlopen(raw_url("sys", "sys/config/config.json")) as response:
                remote_config = response.read().decode("utf-8")
            with open(config_path, "w") as f:
                f.write(remote_config)
            print("config.json Updated successfully")
            updated_any = True
        except Exception:
            pass

        if not updated_any:
            print("All packages up to date")

    else:
        print("Invalid flag. Use -S to install, -R to remove, -U to update installed packages, or -Ua to update installed packages + sys branch.")
