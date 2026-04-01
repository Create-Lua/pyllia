def run(args, shell_state):
    try:
        expr = " ".join(args)
        print(eval(expr))
    except Exception as e:
        print(f"Error: {e}")
