# Copyright (C) 2021 Biren Patel
# MIT License
# Tree walk interpreter

from src.error import ErrorHandler
from src.node import Binary, Unary, Literal, Grouping
from src.tokenizer import Token, TokenType

class RuntimeError(Exception):
    """\
    handles lox runtime errors that occur as the interpreter unwinds.
    """
    pass

class Interpreter():
    def __init__(self):
        self.err = ErrorHandler(1)

    def interpret(self, node):
        """\
        depth-first post-order traversal of abstract syntax tree
        """
        try:
            return (self.traverse(node), self.err)
        except RuntimeError:
            return (None, self.err)
        except KeyError:
            #suppress call stack and surface the error via the lox handler
            name = node.__class__.__name__
            msg = "(INTERNAL ERROR) node {} not in jump table".format(name)
            self.err.push(-1, msg)
            return (None, self.err)

    def traverse(self, node):
        """\
        centralized switch mechanism. All node handlers relegate child node
        traversal to this function since python 3.9 does not have switches or
        pattern matching.
        """
        return Interpreter.jmp_table[node.__class__.__name__](self, node)

    def handle_binary(self, node):
        """\
        evaluate binary nodes where both lval and rval must be a number. If the
        operator is addition, then both lval and rval may be a string. equality
        operators may support any mixed types.
        """
        lval = self.traverse(node.left)
        rval = self.traverse(node.right)

        if node.operator.type == TokenType.EQUAL_EQUAL:
            return lval == rval
        elif node.operator.type == TokenType.BANG_EQUAL:
            return lval != rval
        elif node.operator.type == TokenType.PLUS:
            if isinstance(lval, float) and isinstance(rval, float):
                return lval + rval
            elif isinstance(lval, str) and isinstance(rval, str):
                return lval + rval
        else:
            if isinstance(lval, float) and isinstance(rval, float):
                return Interpreter.bin_table[node.operator.type](lval, rval)

        line = node.operator.line
        msg = "cannot perform {} on mismatched types of {} and {}".format(\
               node.operator.lexeme, lval, rval)
        self.err.push(msg)
        raise RuntimeError

    def handle_unary(self, node):
        """\
        evaluate unary node where operand of '-' must be a number and operands
        of '!' evaluate to False only when operand is 'nil' or 'false'
        """
        val = self.traverse(node.right)

        if node.operator.type == TokenType.MINUS:
            if isinstance(val, float):
                return -1 * float(val)

            line = node.operator.line
            msg = "operand of '-' must be a number"
            self.err.push(line, msg)
            raise RuntimeError

        elif node.operator.type == TokenType.BANG:
            if val == None or val == False:
                return True

            return False

    def handle_literal(self, node):
        """\
        access unmodified literal value field in token at the literal node. This
        value was already generated as a byproduct of the tokenization phase.
        """
        return node.val.literal

    def handle_grouping(self, node):
        """\
        interpret a grouped node "(" <expr> ")"
        """
        return self.traverse(node.val)

    #class variable
    #
    #Required since python 3.9 does not have switches or pattern matching.
    #The methods could have been implemented into each node class itself. But,
    #the lox error handler is easier to use if we dispatch from here. I also
    #prefer to treat the tree nodes as data bags as we did with lexer tokens.
    #This way, the design is consistent and functionality is relegated to
    #functions rather than hidden as methods in return values of functions.
    #source -> f(source) -> tokens -> f(tokens) -> nodes -> f(nodes)

    jmp_table = {
        'Binary':   handle_binary,
        'Unary':    handle_unary,
        'Literal':  handle_literal,
        'Grouping': handle_grouping
    }

    #dispatch for binary node evaluation
    bin_table = {
        TokenType.MINUS:            lambda x, y: x - y,
        TokenType.STAR:             lambda x, y: x * y,
        TokenType.SLASH:            lambda x, y: x / y,
        TokenType.GREATER:          lambda x, y: x > y,
        TokenType.LESS:             lambda x, y: x < y,
        TokenType.GREATER_EQUAL:    lambda x, y: x >= y,
        TokenType.LESS_EQUAL:       lambda x, y: x <= y,
    }
