import os

def run(args, shell_state):
    cwd = shell_state["current_dir"]

    if not args:
        print(cwd)
        return

    target = args[0]
    new_dir = os.path.join(cwd, target) if target != ".." else os.path.dirname(cwd)

    if os.path.isdir(new_dir):
        shell_state["current_dir"] = os.path.abspath(new_dir)
        print(f"Changed directory to: {shell_state['current_dir']}")
    else:
        print(f"No such directory: {target}")