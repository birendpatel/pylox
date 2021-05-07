# Copyright (C) 2021 Biren Patel
# MIT License
# Tree walk interpreter

from src.error import ErrorHandler, RuntimeError
from src.node import Binary, Unary, Literal, Grouping

class Interpreter():
    def __init__(self):
        self.err = ErrorHandler(1)

    def interpret(self, node):
        """\
        depth-first post-order traversal of abstract syntax tree
        """
        try:
            return (self.expression(node), self.err)
        except RuntimeError:
            return (None, self.err)
        except KeyError:
            #suppress the python call stack
            #instead, surface the error via the lox handler
            name = node.__class__.__name__
            msg = "(INTERNAL ERROR) node {} not in jump table".format(name)
            self.err.push(-1, msg)
            return (None, self.err)

    def expression(self, node):
        return node.interpret(self.err)
