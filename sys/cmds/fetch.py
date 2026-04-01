import os
import urllib.request
import json

def run(args, shell_state):
    if len(args) < 1:
        print("Usage: fetch -S|-R|-U|-Ua <package_name>")
        return

    flag = args[0]
    cmds_dir = os.path.join(shell_state["current_dir"], "cmds")
    if not os.path.exists(cmds_dir):
        os.mkdir(cmds_dir)

    installed_packages = [
        f for f in os.listdir(cmds_dir)
        if f.endswith(".py") and f != "fetch.py"
    ]

    repo_user = "Create-Lua"
    repo_name = "pkgshrimp-repo"

    def raw_url(branch, filename):
        return f"https://raw.githubusercontent.com/{repo_user}/{repo_name}/{branch}/{filename}"

    def fetch_sys_files():
        api_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/contents?ref=sys"
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.load(response)
            return [f["name"] for f in data if f["name"].endswith(".py")]
        except Exception as e:
            print(f"Failed to fetch sys branch files: {e}")
            return []

    # ------------------- INSTALL -------------------
    if flag == "-S":
        if len(args) < 2:
            print("Usage: fetch -S <package_name>")
            return
        package = args[1]
        dest_path = os.path.join(cmds_dir, f"{package}.py")
        try:
            urllib.request.urlretrieve(raw_url("main", f"{package}.py"), dest_path)
            print(f"{package} installed/reinstalled successfully to cmds/")
        except Exception as e:
            print(f"Failed to download {package}: {e}")

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
            print(f"{package} removed successfully from cmds/")
        except Exception as e:
            print(f"Failed to remove {package}: {e}")

    # ------------------- UPDATE -------------------
    elif flag == "-U":
        if not installed_packages:
            print("No packages installed to update.")
            return
        for pkg_file in installed_packages:
            file_url = raw_url("main", pkg_file)
            dest_path = os.path.join(cmds_dir, pkg_file)
            try:
                urllib.request.urlretrieve(file_url, dest_path)
                print(f"{pkg_file[:-3]} updated successfully from main branch.")
            except Exception:
                pass

    # ------------------- UPDATE + SYS -------------------
    elif flag == "-Ua":
        # Step 1: Update installed main packages
        for pkg_file in installed_packages:
            file_url = raw_url("main", pkg_file)
            dest_path = os.path.join(cmds_dir, pkg_file)
            try:
                urllib.request.urlretrieve(file_url, dest_path)
                print(f"{pkg_file[:-3]} updated successfully from main branch.")
            except Exception:
                pass

        # Step 2: Download all sys branch files (overwrite existing ones)
        sys_files = fetch_sys_files()
        for sys_file in sys_files:
            if sys_file == "Terminal.py":
                dest_path = os.path.join(shell_state["current_dir"], "Terminal.py")
            else:
                dest_path = os.path.join(cmds_dir, sys_file)
            try:
                urllib.request.urlretrieve(raw_url("sys", sys_file), dest_path)
                print(f"{sys_file[:-3]} downloaded/updated from sys branch.")
            except Exception:
                print(f"{sys_file[:-3]} skipped (could not download).")

    else:
        print("Invalid flag. Use -S to install/reinstall, -R to remove, -U to update installed packages, or -Ua to update installed packages + sys branch.")
