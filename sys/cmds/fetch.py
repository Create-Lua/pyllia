__version__ = "1.2"

import os
import json
import urllib.request

# ----------------------------
# Repo settings
# ----------------------------
repo_user = "Create-Lua"
repo_name = "pyllia"  # your repo name

# ----------------------------
# Helper functions
# ----------------------------
def raw_url(branch, filepath):
    return f"https://raw.githubusercontent.com/{repo_user}/{repo_name}/{branch}/{filepath}"

def get_remote_version(url):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
        return None
    except Exception:
        return None

def get_local_version(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
        return None
    except Exception:
        return None

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

    installed_packages = [f for f in os.listdir(cmds_dir) if f.endswith(".py") and f != "fetch.py"]

    # ------------------- INSTALL -------------------
    if flag == "-S":
        if len(args) < 2:
            print("Usage: fetch -S <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        remote_ver = get_remote_version(raw_url("main", f"cmds/{package}.py"))
        local_ver = get_local_version(dest_path)
        if remote_ver is None:
            print("Package not found")
            return
        if local_ver is None or remote_ver > local_ver:
            try:
                urllib.request.urlretrieve(raw_url("main", f"cmds/{package}.py"), dest_path)
                print(f"{package} Installed/Updated successfully")
            except Exception as e:
                print(f"Failed to download {package}: {e}")
        else:
            print(f"{package} is already up to date")

    # ------------------- REMOVE -------------------
    elif flag == "-R":
        if len(args) < 2:
            print("Usage: fetch -R <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        if not os.path.exists(dest_path):
            print(f"No such package installed: {package}")
            return
        try:
            os.remove(dest_path)
            print(f"{package} removed successfully")
        except Exception as e:
            print(f"Failed to remove {package}: {e}")

    # ------------------- UPDATE -------------------
    elif flag == "-U":
        updated_any = False
        for pkg_file in installed_packages:
            local_path = os.path.join(cmds_dir, pkg_file)
            remote_ver = get_remote_version(raw_url("main", f"cmds/{pkg_file}"))
            local_ver = get_local_version(local_path)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                try:
                    urllib.request.urlretrieve(raw_url("main", f"cmds/{pkg_file}"), local_path)
                    print(f"{pkg_file[:-3]} Updated successfully")
                    updated_any = True
                except Exception as e:
                    print(f"Failed to update {pkg_file[:-3]}: {e}")
        if not updated_any:
            print("All packages up to date")

    # ------------------- UPDATE + SYS -------------------
    elif flag == "-Ua":
        updated_any = False

        # Step 1: Update all sys commands
        sys_cmds_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/contents/sys/cmds"
        try:
            with urllib.request.urlopen(sys_cmds_url) as response:
                data = json.load(response)
            sys_files = [f["name"] for f in data if f["name"].endswith(".py")]
        except Exception:
            sys_files = []

        for cmd_file in sys_files:
            dest_path = os.path.join(cmds_dir, cmd_file)
            remote_ver = get_remote_version(raw_url("sys/cmds", cmd_file))
            local_ver = get_local_version(dest_path)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                try:
                    urllib.request.urlretrieve(raw_url("sys/cmds", cmd_file), dest_path)
                    print(f"{cmd_file[:-3]} Updated successfully")
                    updated_any = True
                except Exception as e:
                    print(f"Failed to update {cmd_file[:-3]}: {e}")

        # Step 2: Terminal.py
        remote_ver = get_remote_version(raw_url("sys", "Terminal.py"))
        local_ver = get_local_version(terminal_path)
        if remote_ver and (local_ver is None or remote_ver > local_ver):
            try:
                urllib.request.urlretrieve(raw_url("sys", "Terminal.py"), terminal_path)
                print("Terminal.py Updated successfully")
                updated_any = True
            except Exception as e:
                print(f"Failed to update Terminal.py: {e}")

        # Step 3: config.json
        config_path = os.path.join(config_dir, "config.json")
        try:
            with urllib.request.urlopen(raw_url("sys/config", "config.json")) as response:
                remote_config = response.read().decode("utf-8")
            remote_data = json.loads(remote_config)
            remote_ver = remote_data.get("version", None)
        except Exception:
            remote_ver = None

        try:
            local_data = {}
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    local_data = json.load(f)
            local_ver = local_data.get("version", None)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                with open(config_path, "w") as f:
                    f.write(remote_config)
                print("config.json Updated successfully")
                updated_any = True
        except Exception as e:
            print(f"Failed to update config.json: {e}")

        if not updated_any:
            print("All packages up to date")

    else:
        print("Invalid flag. Use -S to install, -R to remove, -U to update installed packages, or -Ua to update installed packages + sys branch.")
