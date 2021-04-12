# Copyright (C) 2021, Biren Patel
# MIT License
# Convert lox raw source code to a list of tokens

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

#inverse mapping of single/double tokens from TokenType
double_map = {
'!': TokenType.BANG,
'!=': TokenType.BANG_EQUAL,
'=': TokenType.EQUAL,
'==': TokenType.EQUAL_EQUAL,
'>': TokenType.GREATER,
'>=': TokenType.GREATER_EQUAL,
'<': TokenType.LESS,
'<=': TokenType.LESS_EQUAL,
}

#whitespace characters excluding newline and comments
whitespace_set = set([' ', '\t', '\r', '\f', '\v'])

#tokenizer single/double tokens helper function
def handle_double(i, line, src, tokens) -> int:
    double = src[i] + src[i + 1]

    if double in double_map:
        tokens.append(Token(double_map[double], line, double, None))
        i += 1
    else:
        tokens.append(Token(double_map[src[i]], line, src[i], None))

    return i

#tokenizer slash helper function
#i is the index of the last-parsed character belonging to the comment
def handle_slash(i, line, src, tokens) -> int:
    if src[i + 1] == '/':
        i = i + src[i:].find('\n') - 1
        assert(i > 0 and "str.find retval is not -1")
    else:
        tokens.append(Token(TokenType.SLASH, line, '/', None))

    return i

#tokenizer string literal helper function, returns negative as an error signal
#return index of closing quotation
def handle_string(i, line, src, tokens) -> int:
    quote = src[i + 1:].find('"')
    newline = src[i + 1:].find('\n')

    if quote != -1 and quote < newline:
        lexeme = src[i: quote + 2]
        literal = src[i + 1: quote + 1]
        tokens.append(Token(TokenType.STRING, line, lexeme, literal))
    else:
        return -1

    return i + quote + 1

#via pylox.py tokenizer always expects a newline terminated input
#therefore no try-catch for IndexError required for src[i + 1] access
def tokenize(src):
    """\
    convert input source string into a List[Token]
    """
    tokens = []
    err = ErrorHandler(limit = 3)

    line = 1
    i = 0

    while i < len(src):
        assert(i >= 0 and "index is not strictly increasing")
        assert(line >= 1 and "line is not strictly increasing")

        if src[i] in single_map:
            tokens.append(Token(single_map[src[i]], line, src[i], None))
        elif src[i] in double_map:
            i = handle_double(i, line, src, tokens)
        elif src[i] in whitespace_set:
            pass
        elif src[i] == '\n':
            line += 1
        elif src[i] == '/':
            i = handle_slash(i, line, src, tokens)
        elif src[i] == '"':
            i = handle_string(i, line, src, tokens)

            if i < 0:
                err.grow(1)
                status = err.push(line, 'string not terminated')
                break
        else:
            if not err.push(line, 'found unknown symbol {}'.format(src[i])):
                err.grow(1)
                err.push(line, 'additional errors found (hidden)')
                break

        i += 1

    if not err:
        tokens.append(Token(TokenType.EOF, line, None, None))

    #if there are no errors then tokens must be nonempty
    assert(bool(err) == True or bool(tokens) == True)

    return (tokens, err)
