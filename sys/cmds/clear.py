__version__ = "1.0"

import os
import platform

def run(args, shell_state):
    # Determine the OS
    system_name = platform.system()

    try:
        if system_name == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as e:
        print(f"Error clearing screen: {e}")
