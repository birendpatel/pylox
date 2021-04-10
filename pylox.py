# Copyright (C) 2021, Biren Patel
# MIT License

from sys import argv

# lox repl
def exec_prompt() -> None:
    while(True):
        try:
            src = input(">>> ")
            run(src)
        except (KeyboardInterrupt, EOFError):
            print("")
            break

# fetch lox source from file
def exec_file(fname: str) -> None:
    try:
        with open(fname, 'r') as file:
            src: str = file.read()
            run(src)
    except FileNotFoundError:
        print("{} file not found".format(fname))

#execute lox source code
def run(src: str) -> None:
    print(src)

if __name__ == "__main__":
    argc: int = len(argv)

    if (argc == 1):
        exec_prompt()
    elif (argc == 2):
        exec_file(argv[1])
    else:
        print("usage: python3 pylox.py [script]")
