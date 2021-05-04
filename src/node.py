# Copyright (C) 2021 Biren Patel
# MIT License
# abstract syntax tree node classes
#
# Unlike the textbook source, pylox doesn't implement a visitor class nor does
# it define an interface. We just define each class separately with all the
# required methods. Python's dynamic and duck typing handles the details when
# we need to operate on an AST node.

class Literal():
        def __init__(self, val):
            self.val = val

        def __repr__(self):
            return "{}".format(self.val.lexeme)

class Unary():
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right

        def __repr__(self):
            return "({} {})".format(self.operator.lexeme, self.right)

class Binary():
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        msg = "({} {} {})"
        return msg.format(self.operator.lexeme, self.left, self.right)

class Grouping():
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "(group {})".format(self.val)
