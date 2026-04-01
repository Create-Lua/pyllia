__version__ = "1.0"

import os
import urllib.request
import json
import importlib.util

def run(args, shell_state):
    if len(args) < 1:
        print("Usage: fetch -S|-R|-U|-Ua <package_name>")
        return

    flag = args[0].lower()
    base_dir = shell_state["current_dir"]
    cmds_dir = os.path.join(base_dir, "cmds")
    config_dir = os.path.join(base_dir, "config")
    terminal_path = os.path.join(base_dir, "Terminal.py")

    os.makedirs(cmds_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)

    repo_user = "Create-Lua"
    repo_name = "pyllia"

    def raw_url(folder, filename):
        return f"https://raw.githubusercontent.com/{repo_user}/{repo_name}/main/{folder}/{filename}"

    def get_remote_version(url):
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode("utf-8")
            for line in content.splitlines():
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"\'')
        except Exception:
            return None

    def get_local_version(path):
        if not os.path.exists(path):
            return None
        try:
            spec = importlib.util.spec_from_file_location("temp_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, "__version__", None)
        except Exception:
            return None

    # ------------------- INSTALL -------------------
    if flag == "-s":
        if len(args) < 2:
            print("Usage: fetch -S <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        remote_url = raw_url("fetch-repo", f"{package}.py")
        try:
            remote_ver = get_remote_version(remote_url)
            if remote_ver is None:
                print("Package not found")
                return
            local_ver = get_local_version(dest_path)
            if local_ver is None or remote_ver > local_ver:
                urllib.request.urlretrieve(remote_url, dest_path)
        except Exception as e:
            print(f"Failed to download {package}: {e}")

    # ------------------- REMOVE -------------------
    elif flag == "-r":
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
        except Exception as e:
            print(f"Failed to remove {package}: {e}")

    # ------------------- UPDATE -------------------
    elif flag == "-u":
        for pkg_file in os.listdir(cmds_dir):
            if not pkg_file.endswith(".py") or pkg_file == "fetch.py":
                continue
            local_path = os.path.join(cmds_dir, pkg_file)
            remote_url = raw_url("fetch-repo", pkg_file)
            remote_ver = get_remote_version(remote_url)
            local_ver = get_local_version(local_path)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                try:
                    urllib.request.urlretrieve(remote_url, local_path)
                except Exception as e:
                    print(f"Failed to update {pkg_file[:-3]}: {e}")

    # ------------------- UPDATE + SYS -------------------
    elif flag == "-ua":
        # Step 1: update installed packages
        for pkg_file in os.listdir(cmds_dir):
            if not pkg_file.endswith(".py") or pkg_file == "fetch.py":
                continue
            local_path = os.path.join(cmds_dir, pkg_file)
            remote_url = raw_url("fetch-repo", pkg_file)
            remote_ver = get_remote_version(remote_url)
            local_ver = get_local_version(local_path)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                try:
                    urllib.request.urlretrieve(remote_url, local_path)
                except Exception as e:
                    print(f"Failed to update {pkg_file[:-3]}: {e}")

        # Step 2: update sys commands
        sys_cmds_api = f"https://api.github.com/repos/{repo_user}/{repo_name}/contents/sys/cmds"
        try:
            with urllib.request.urlopen(sys_cmds_api) as response:
                data = json.load(response)
            sys_files = [f["name"] for f in data if f["name"].endswith(".py")]
        except Exception:
            sys_files = []

        for cmd_file in sys_files:
            dest_path = os.path.join(cmds_dir, cmd_file)
            remote_url = raw_url("sys/cmds", cmd_file)
            remote_ver = get_remote_version(remote_url)
            local_ver = get_local_version(dest_path)
            if remote_ver and (local_ver is None or remote_ver > local_ver):
                try:
                    urllib.request.urlretrieve(remote_url, dest_path)
                except Exception as e:
                    print(f"Failed to update {cmd_file[:-3]}: {e}")

        # Step 3: Terminal.py
        remote_ver = get_remote_version(raw_url("sys", "Terminal.py"))
        local_ver = get_local_version(terminal_path)
        if remote_ver and (local_ver is None or remote_ver > local_ver):
            try:
                urllib.request.urlretrieve(raw_url("sys", "Terminal.py"), terminal_path)
            except Exception as e:
                print(f"Failed to update Terminal.py: {e}")

        # Step 4: config.json
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
        except Exception as e:
            print(f"Failed to update config.json: {e}")

    else:
        print("Invalid flag. Use -S to install/reinstall, -R to remove, -U to update installed packages, or -Ua to update installed packages + sys branch.")
