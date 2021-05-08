# Copyright (C) 2021 Biren Patel
# MIT License
# abstract syntax tree node classes for both statements and expressions

from abc import ABC, abstractmethod
from src.error import ErrorHandler, RuntimeError
from src.environment import Environment
from src.tokenizer import Token, TokenType

################################################################################
# expression-type nodes

class expr(ABC):
    """\
    abstract base class of all expression-type nodes.
    """
    @abstractmethod
    def __repr__(self):
        """\
        print AST when preprocessor enforces #pragma parse_debug on
        """
        pass

    @abstractmethod
    def interpret(self, err, env):
        """\
        recursively interpret node and return computed value.
        """
        pass

class Literal(expr):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "{}".format(self.val.lexeme)

    def interpret(self, err, env):
        return self.val.literal

class Variable(expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "{}".format(self.name.lexeme)

    def interpret(self, err, env):
        key = self.name.lexeme

        try:
            return env.search(key)
        except KeyError:
            line = self.name.line
            msg = "undefined variable {}".format(key)
            err.push(line, msg)
            raise RuntimeError

class Unary(expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return "({} {})".format(self.operator.lexeme, self.right)

    def interpret(self, err, env):
        val = self.right.interpret(err, env)

        if self.operator.type == TokenType.MINUS:
            if isinstance(val, float):
                return -1 * float(val)

            line = self.operator.line
            msg = "operand of '-' must be a number"
            err.push(line, msg)
            raise RuntimeError

        elif self.operator.type == TokenType.BANG:
            if val == None or val == False:
                return True

            return False

class Binary(expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        msg = "({} {} {})"
        return msg.format(self.operator.lexeme, self.left, self.right)

    def interpret(self, err, env):
        lval = self.left.interpret(err, env)
        rval = self.right.interpret(err, env)

        type = self.operator.type

        if type in Binary.dispatch_any:
            return Binary.dispatch_any[type](lval, rval)
        elif isinstance(lval, float) and isinstance(rval, float):
            return Binary.dispatch_float[type](lval, rval)
        elif type == TokenType.PLUS:
            if isinstance(lval, str) and isinstance(rval, str):
                return lval + rval

        line = self.operator.line
        lexeme = self.operator.lexeme
        msg = "cannot perform '{}' on mismatched types".format(lexeme)
        err.push(line, msg)
        raise RuntimeError

    dispatch_any = {
        TokenType.EQUAL_EQUAL:      lambda x, y: x == y,
        TokenType.BANG_EQUAL:       lambda x, y: x != y
    }

    dispatch_float = {
        TokenType.PLUS:             lambda x, y: x + y,
        TokenType.MINUS:            lambda x, y: x - y,
        TokenType.STAR:             lambda x, y: x * y,
        TokenType.SLASH:            lambda x, y: x / y,
        TokenType.GREATER:          lambda x, y: x > y,
        TokenType.LESS:             lambda x, y: x < y,
        TokenType.GREATER_EQUAL:    lambda x, y: x >= y,
        TokenType.LESS_EQUAL:       lambda x, y: x <= y,
    }

class Grouping(expr):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "(group {})".format(self.val)

    def interpret(self, err, env):
        return self.val.interpret(err, env)

################################################################################
# statement-type nodes
# these nodes are essentially identical to expression-type nodes but the
# underlying abstract base class allows for helpful isinstance() distinctions
# to be made during parsing and interpretation.

class stmt(ABC):
    """\
    abstract base class of all statement-type nodes
    """
    @abstractmethod
    def __repr__(self):
        """\
        print AST when preprocessor enforces #pragma parse_debug on
        """
        pass

    @abstractmethod
    def interpret(self, err, env):
        """\
        recursively interpret node and return computed value.
        """
        pass

class Generic(stmt):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "(statement {})".format(self.expr)

    def interpret(self, err, env):
        self.expr.interpret(err, env)
        return None

#todo: pretty printing
class Printer(stmt):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "(print {})".format(self.expr)

    def interpret(self, err, env):
        val = self.expr.interpret(err, env)
        print(val)
        return None

class VariableDeclaration(stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        if self.initializer is None:
            return "(= {} nil)".format(self.name)

        return "(= {} {})".format(self.name, self.initializer)

    def interpret(self, err, env):
        pass
