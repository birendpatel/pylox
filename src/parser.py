# Copyright (C) 2021 Biren Patel
# MIT License
# Generate an abstract syntax tree via a recusive descent parser

from src.error import ErrorHandler
from src.tokenizer import Token, TokenType
from src.node import Binary, Unary, Literal, Grouping

class Parser():
    def __init__(self):
        pass

    def parse(self, tokens):
        return (None, None)
