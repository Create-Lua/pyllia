def run(args, shell_state):
    if not args:
        print("Usage: pyllia [--version|--credits]")
        return

    flag = args[0]

    if flag == "--version":
        print("Pyllia version 1.6 Beta")

    elif flag == "--credits":
        print("Pyllia created by Alex")
    
    elif flag == "--cow":
        print("((...))")
        print("( o o )")
        print(" \   /")
        print("  ^_^")

    else:
        print("Invalid usage.")
