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

    def expression(self, node):
        return node.interpret(self.err)
