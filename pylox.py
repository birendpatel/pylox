# Copyright (C) 2021, Biren Patel
# MIT License

from src.error import ErrorHandler
from src.interpreter import Interpreter
from src.parser import Parser
from src.preprocessor import Preprocessor
from src.tokenizer import Token, TokenType, Tokenizer
from sys import argv

# lox repl
def exec_prompt() -> None:
    while(True):
        try:
            src = input(">>> ") + '\n'
            run(src)
        except (KeyboardInterrupt, EOFError):
            print("\b\b  ")
            break

# fetch lox source from file
def exec_file(fname: str) -> None:
    try:
        with open(fname, 'r') as file:
            p_src: str = file.read()

            if p_src[-1] != '\n':
                p_src += '\n'

            src = preprocess(p_src)
            run(src)
    except FileNotFoundError:
        print("{} file not found".format(fname))

#execute preprocessor
def preprocess(p_src: str) -> str:
    global tok_debug
    global parse_debug

    pps = Preprocessor()
    src, flags = pps.scan(p_src)

    tok_debug = flags["tok_debug"]
    parse_debug = flags["parse_debug"]

    return src

#execute lox source code
def run(src: str) -> None:
    #tokenization
    tkz = Tokenizer()
    tokens, err = tkz.tokenize(src)

    if display_errors(err, "LOX: SYNTAX ERROR"):
        return

    if tok_debug:
        for i in tokens:
            print(i)

    #don't send single EOF token to parser
    #this allows parser to make stricter assertions while generating the AST
    if tokens[0].type == TokenType.EOF:
        return

    #parsing
    prs = Parser()
    program, err = prs.parse(tokens)

    if display_errors(err, "LOX: GRAMMAR ERROR"):
        return

    if parse_debug:
        for tree in program:
            print(tree)

    #interpretation
    itr = Interpreter()
    val, err = itr.interpret(program)
    display_errors(err, "LOX: RUNTIME ERROR")

#error trap
def display_errors(err, header) -> bool:
    if err:
        print(header)

        for i in err:
            print("\t{}".format(i))

        return True

    return False

#lox entry point, repl or source
if __name__ == "__main__":
    tok_debug = False
    parse_debug = False

    argc: int = len(argv)

    if (argc == 1):
        exec_prompt()
    elif (argc == 2):
        exec_file(argv[1])
    else:
        print("usage: python3 pylox.py [script]")
