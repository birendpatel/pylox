# Copyright (C) 2021, Biren Patel
# MIT License
# Convert lox raw source code to a list of tokens

from dataclasses import dataclass
from enum import Enum
from src.error import ErrorHandler

class TokenType(Enum):
    """\
    All tokens, keywords, and literals allowed in source by the lox language
    """
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'
    EOF = 'EOF'
    IDENTIFIER = 'xyz'
    STRING = 'abc'
    NUMBER = '123'

class Token():
    def __init__(self, type, line, lexeme, literal):
        """\
        @type: see class TokenType
        @line: line number where token was found
        @lexeme: raw source code textual representations
        @literal: runtime value of number and string representatios
        """
        self.type = type
        self.line = line
        self.lexeme = lexeme
        self.literal = literal

    def __repr__(self):
        msg = "line {}: {} ({},{})"
        return msg.format(self.line, self.type, self.lexeme, self.literal)

#inverse mapping of single charcter tokens from TokenType, except slash
single_map = {
'(': TokenType.LEFT_PAREN,
')': TokenType.RIGHT_PAREN,
'{': TokenType.LEFT_BRACE,
'}': TokenType.RIGHT_BRACE,
',': TokenType.COMMA,
'.': TokenType.DOT,
'-': TokenType.MINUS,
'+': TokenType.PLUS,
';': TokenType.SEMICOLON,
'*': TokenType.STAR
}

#whitespace characters excluding newline and comments
white_set = set([' ', '\t', '\r', '\f', '\v'])

def tokenize(src):
    """\
    convert input source string into a List[Token]
    """
    tokens = []
    err = ErrorHandler(limit = 3)

    line = 0
    i = 0

    while i < len(src):
        if src[i] in single_map:
            tokens.append(Token(single_map[src[i]], line, src[i], None))
            i += 1
            continue
        elif src[i] in white_set:
            i += 1
            continue
        else:
            status = err.push(line, 'found unknown symbol {}'.format(src[i]))

            if status == False:
                err.grow(1)
                err.push(line, 'additional errors found (hidden)')
                break
            else:
                i = i + 1

    if not err:
        tokens.append(Token(TokenType.EOF, line, None, None))

    return (tokens, err)
