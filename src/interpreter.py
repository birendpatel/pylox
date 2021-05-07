# Copyright (C) 2021 Biren Patel
# MIT License
# Tree walk interpreter

from src.error import ErrorHandler, RuntimeError
from src.node import Binary, Unary, Literal, Grouping
from src.node import Generic, Printer

class Interpreter():
    def __init__(self):
        self.err = ErrorHandler(1)

    def interpret(self, program):
        """\
        depth-first post-order traversal of program tree
        """
        for tree in program:
            try:
                tree.interpret(self.err)
                return (0, self.err)
            except RuntimeError:
                return (1, self.err)
