# Copyright (C) 2021 Biren Patel
# MIT License
# abstract syntax tree node classes

from abc import ABC

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
    def interpret(self, err):
        """\
        recursively interpret node and return computed value.
        """
        pass

class Literal():
        def __init__(self, val):
            self.val = val

        def __repr__(self):
            return "{}".format(self.val.lexeme)

        def interpret(self, err):
            return self.val.literal

class Unary():
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right

        def __repr__(self):
            return "({} {})".format(self.operator.lexeme, self.right)

        def interpret(self, err):
            val = self.right.interpret()

            if self.operator.type == TokenType.MINUS:
                if isinstance(val, float):
                    return -1 * float(val)

                line = self.operator.line
                msg = "operand of '-' must be a number"
                self.err.push(line, msg)
                raise RuntimeError

            elif self.operator.type == TokenType.BANG:
                if val == None or val == False:
                    return True

                return False

class Binary():
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        msg = "({} {} {})"
        return msg.format(self.operator.lexeme, self.left, self.right)

    def interpret(self, err):
        lval = self.left.interpret()
        rval = self.right.interpret()

        if self.operator.type == TokenType.EQUAL_EQUAL:
            return lval == rval
        elif self.operator.type == TokenType.BANG_EQUAL:
            return lval != rval
        elif self.operator.type == TokenType.PLUS:
            if isinstance(lval, float) and isinstance(rval, float):
                return lval + rval
            elif isinstance(lval, str) and isinstance(rval, str):
                return lval + rval
        else:
            if isinstance(lval, float) and isinstance(rval, float):
                return Binary.dispatch(self.operator.type)(lval, rval)

        line = self.operator.line
        msg = "cannot perform {} on mismatched types of {} and {}".format(\
               self.operator.lexeme, lval, rval)
        self.err.push(line, msg)
        raise RuntimeError


    dispatch = {
        TokenType.MINUS:            lambda x, y: x - y,
        TokenType.STAR:             lambda x, y: x * y,
        TokenType.SLASH:            lambda x, y: x / y,
        TokenType.GREATER:          lambda x, y: x > y,
        TokenType.LESS:             lambda x, y: x < y,
        TokenType.GREATER_EQUAL:    lambda x, y: x >= y,
        TokenType.LESS_EQUAL:       lambda x, y: x <= y,
    }

class Grouping():
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "(group {})".format(self.val)

    def interpret(self, err):
        return self.val.interpret()
