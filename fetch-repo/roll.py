import random
def run(args, shell_state):
    sides = int(args[0]) if args else 6
    print(random.randint(1, sides))
