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

class Tokenizer():
    def __init__(self):
        """\
        convert input source string into a List[Token]
        """
        self.src = " "
        self.err = ErrorHandler()
        self.line = 0
        self.i = 0 #src index
        self.tokens = []

        #inverse mapping of single char TokenTypes, except slash
        self.single_map = {
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
        self.double_map = {
        '!': TokenType.BANG,
        '!=': TokenType.BANG_EQUAL,
        '=': TokenType.EQUAL,
        '==': TokenType.EQUAL_EQUAL,
        '>': TokenType.GREATER,
        '>=': TokenType.GREATER_EQUAL,
        '<': TokenType.LESS,
        '<=': TokenType.LESS_EQUAL,
        }

        #inverse mapping of keywords from TokenType
        self.keywords_map = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'fun': TokenType.FUN,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
        }

        #whitespace characters excluding newline and comments
        self.whitespace_set = set([' ', '\t', '\r', '\f', '\v'])

        #digit characters
        self.digit_set = set(['0','1','2','3','4','5','6','7','8','9'])

    def handle_double(self):
        """\
        single/double tokens helper for self.tokenize
        """
        double = self.src[self.i] + self.src[self.i + 1]

        if double in self.double_map:
            tok = Token(self.double_map[double], self.line, double, None)
            self.tokens.append(tok)
            self.i += 1
        else:
            char = self.src[self.i]
            tok = Token(self.double_map[char], self.line, char, None)
            self.tokens.append(tok)

    def handle_digit(self):
        """\
        number literals helper for self.tokenize.
        sets self.i to negative on error.
        """
        j = self.i

        while self.src[j] in self.digit_set:
            j += 1

            if self.src[j] == '.':
                if self.src[j + 1] in self.digit_set:
                    j += 1
                else:
                    self.i = -1
                    return

        lexeme = self.src[self.i:j]
        literal = float(lexeme)
        tok = Token(TokenType.NUMBER, self.line, lexeme, literal)
        self.tokens.append(tok)

        self.i = j - 1

    def handle_slash(self):
        """\
        slash and comments helper for self.tokenize.
        i is set to the index of the last-parsed charcter of the comment
        """
        if self.src[self.i + 1] == '/':
            self.i = self.i + self.src[self.i:].find('\n') - 1
            assert(self.i > 0 and "str.find retval is not -1")
        else:
            tok = Token(TokenType.SLASH, self.line, '/', None)
            self.tokens.append(tok)

    def handle_string(self):
        """\
        string literal helper function for self.tokenize.
        sets i to negative on error, else i is index of closing quotation
        """
        quote = self.src[self.i + 1:].find('"')
        newline = self.src[self.i + 1:].find('\n')

        if quote != -1 and quote < newline:
            lexeme = self.src[self.i: self.i + quote + 2]
            literal = self.src[self.i + 1: self.i + quote + 1]
            tok = Token(TokenType.STRING, self.line, lexeme, literal)
            self.tokens.append(tok)
        else:
            self.i = -1

        self.i = self.i + quote + 1

    def handle_word(self):
        """\
        identifier and keywords helper function for self.tokenize.
        returns the word for futher analysis.
        i is set to last char in the identifier/keyword
        """
        j = self.i
        id = self.src

        while id[j].isalpha() or id[j].isdigit() or id[j] == '_':
            j += 1

        word = self.src[self.i:j]
        self.i = j - 1

        if word in self.keywords_map:
            #for keyword 'nil', literal = None is the actual literal value
            tok = Token(self.keywords_map[word], self.line, word, None)

            #add literal values for true/false to assist the interpreter
            #lox bools will reduce to python bools
            if tok.TokenType == TokenType.TRUE
                tok.literal = True
            elif tok.TokenType == TokenType.FALSE
                tok.literal = False

            self.tokens.append(tok)
        else:
            tok = Token(TokenType.IDENTIFIER, self.line, word, word)
            self.tokens.append(tok)

    #via pylox.py tokenizer always expects a newline terminated input
    #therefore no try-catch for IndexError required for src[i + 1] access
    def tokenize(self, src, limit = 3):
        """\
        @src: source code, newline terminated so that src[i + 1] is valid
        @limit: internal ErrorHandler limit
        """
        #reset attrs on multiple calls
        self.src = src
        self.err = ErrorHandler(limit)
        self.line = 1
        self.i = 0
        self.tokens = []

        while self.i < len(self.src):
            assert(self.i >= 0 and "index is not strictly increasing")
            assert(self.line >= 1 and "line is not strictly increasing")

            if (char := self.src[self.i]) in self.single_map:
                tok = Token(self.single_map[char], self.line, char, None)
                self.tokens.append(tok)
            elif self.src[self.i] in self.double_map:
                self.handle_double()
            elif self.src[self.i] in self.whitespace_set:
                pass
            elif self.src[self.i] == '\n':
                self.line += 1
            elif self.src[self.i] == '/':
                self.handle_slash()
            elif self.src[self.i] in self.digit_set:
                self.handle_digit()

                if self.i < 0:
                    self.err.grow(1)
                    self.err.push(line, 'number formatted incorrectly')
                    break
            elif self.src[self.i] == '"':
                self.handle_string()

                if self.i < 0:
                    self.err.grow(1)
                    self.err.push(line, 'string not terminated')
                    break
            elif self.src[self.i].isalpha() or self.src[self.i] == '_':
                self.handle_word()
            else:
                msg = "unknown symbol {}".format(self.src[self.i])

                if not self.err.push(self.line, msg):
                    self.err.grow(1)
                    self.err.push(self.line, 'additional errors found (hidden)')
                    break

            self.i += 1

        #place EOF synthetically on previous line
        if not self.err:
            self.tokens.append(Token(TokenType.EOF, self.line - 1, None, None))

        #if there are no errors then tokens must be nonempty
        assert(bool(self.err) == True or bool(self.tokens) == True)

        return (self.tokens, self.err)
