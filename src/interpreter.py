# Copyright (C) 2021 Biren Patel
# MIT License
# Tree walk interpreter

from src.error import ErrorHandler
from src.node import Binary, Unary, Literal, Grouping

class RuntimeError(Exception):
    """\
    handles lox runtime errors that occur as the interpreter unwinds.
    """
    pass

class Interpreter():
    jmp_table = {
        'Binary': Interpreter.handle_binary,
        'Unary': Interpreter.handle_unary,
        'Literal': Interpreter.handle_literal,
        'grouping': Interpreter.handle_grouping
    }

    def __init__(self):
        self.err = ErrorHandler(1)

    def interpret(self, node):
        try:
            func = jmp_table[node.__class__.__name__]
            val = func(self, node)
            return (val, err)
        except RuntimeError:
            return (None, err)
        except KeyError:
            name = node.__class__.__name__
            msg = "(INTERNAL ERROR) node ({}) not in jump table".format(name)
            err.push(-1, msg)
            return (None, err)

    def handle_binary(self, node):
        pass

    def handle_unary(self, node):
        pass

    def handle_literal(self, node):
        pass

    def handle_grouping(self, node):
        pass
