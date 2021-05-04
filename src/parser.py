# Copyright (C) 2021 Biren Patel
# MIT License
# Generate an abstract syntax tree via a recusive descent parser

from src.error import ErrorHandler
from src.tokenizer import Token, TokenType
from src.node import Binary, Unary, Literal, Grouping

class Parser():
    def __init__(self):
        """\
        convert a list of tokens to an abstract syntax tree
        """
        self.err = ErrorHandler()
        self.tokens = []
        self.ast = None

    def parse(self, tokens, limit = 3):
        """\
        recursive descent entry point
        @tokens: list of tokens provided by lexical analysis, tokens[-1] == EOF
        @limit: internal ErrorHandler limit
        """
        self.err = ErrorHandler(limit)
        self.tokens = tokens
        self.ast = self.expression()

    def expression():
        """\
        dummy method used to encode the lox grammar explicity in the source
        """
        return self.equality():

    def equality():
        pass

    def comparison():
        pass

    def term():
        pass

    def factor():
        pass

    def unary():
        pass

    def primary():
        pass
