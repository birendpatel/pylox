# Copyright (C) 2021 Biren Patel
# MIT License
# Tree walk interpreter

from src.error import ErrorHandler, RuntimeError
from src.environment import Environment
from src.node import Binary, Unary, Literal, Grouping
from src.node import Generic, Printer

class Interpreter():
    def __init__(self, env):
        self.err = ErrorHandler(1)

        if env:
            self.env = env
        else:
            self.env = Environment(None)

    def interpret(self, program):
        """\
        depth-first post-order traversal of program tree
        """
        for tree in program:
            try:
                tree.interpret(self.err, self.env)
            except RuntimeError:
                assert(self.env.parent is None)
                return (1, self.err, self.env)

        assert(self.env.parent is None)
        return (0, self.err, self.env)
