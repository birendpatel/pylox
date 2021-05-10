# Copyright (C) 2021 Biren Patel
# MIT License
# Generate an abstract syntax tree via a recusive descent parser

from src.error import ErrorHandler, ParseError
from src.tokenizer import Token, TokenType

from src.node import Binary, Unary, Variable, Literal, Grouping, Assignment
from src.node import Logical

from src.node import Generic, Printer, VariableDeclaration, Block, Branch
from src.node import Loop

class Parser():
    def __init__(self):
        """\
        convert a list of tokens to an abstract syntax tree
        @i: tokens index
        @ast: abstract syntax tree generated by self.expression()
        """
        self.err = ErrorHandler()
        self.tokens = []
        self.i = 0
        self.ast = None

    def parse(self, tokens, limit = 10):
        """\
        recursive descent entry point

        @tokens: list of tokens provided by lexical analysis, tokens[-1] == EOF
        @limit: internal ErrorHandler limit
        Returns: abstract syntax tree, top level is a list of statements
        """
        self.err = ErrorHandler(limit)
        self.tokens = tokens
        self.i = 0

        try:
            return (self.program(), self.err)
        except ParseError:
            return (None, self.err)

    def curr_type(self):
        """\
        helper function: returns token type of token at current list index
        """
        token = self.tokens[self.i]
        return token.type

    def curr_token(self):
        """\
        helper function: syntactic sugar to fetch current token
        """
        return self.tokens[self.i]

    def advance(self):
        """\
        helper function: syntactic sugar for iteration over the tokens list
        """
        assert(self.i + 1 < len(self.tokens))
        self.i += 1

    def prev_token(self):
        """\
        helper function: syntactic sugar to fetch previous token
        """
        assert(self.i - 1 >= 0)
        return self.tokens[self.i - 1]

    def check_semicolon(self):
        if self.curr_type() == TokenType.SEMICOLON:
            self.advance()
        else:
            tok = self.curr_token()
            if tok.type == TokenType.EOF:
                self.trap("expected ';' at end of file")
            else:
                self.trap("expected ';' before {}".format(tok.lexeme))

    def program(self):
        """\
        <program> := <declaration>* EOF
        """
        tree = []

        while self.curr_type() != TokenType.EOF:
            tree.append(self.declaration())

        assert(self.curr_type() == TokenType.EOF)
        return tree

    def declaration(self):
        """\
        <declaration> := <variable declaration> | <statement>
        """
        if self.curr_type() == TokenType.VAR:
            self.advance()
            return self.var_declaration()

        return self.statement()

    def var_declaration(self):
        """\
        <var_declaration> := "var" IDENTIFIER ("=" <expression>)? ";"
        """
        name = None

        #if no initializer is present, assume that there was actually
        #an intializer to nil, i.e., var x = nil; instead of var x;
        initializer = Literal(Token(TokenType.NIL, -1, "nil", None))

        if self.curr_type() == TokenType.IDENTIFIER:
            name = self.curr_token()
            self.advance()

            if self.curr_type() == TokenType.EQUAL:
                self.advance()
                initializer = self.expression()

            self.check_semicolon()
        else:
            self.trap("missing variable identifier")

        return VariableDeclaration(name, initializer)

    def statement(self):
        """\
        <statement> := <expression statement> | <print statement> |
                       <block statement> | <if statement> | <while statement>
        """
        # this isn't the world's fastest code, a jump table or dictionary-based
        # switch would be better, but hey we're writing an interpreter in
        # python! This is hardly the bottleneck!

        if self.curr_type() == TokenType.PRINT:
            self.advance()
            stmt = self.print_stmt()
        elif self.curr_type() == TokenType.LEFT_BRACE:
            self.advance()
            stmt_list = self.block_stmt()
            stmt = Block(stmt_list)
        elif self.curr_type() == TokenType.IF:
            self.advance()
            stmt = self.branch_stmt()
        elif self.curr_type() == TokenType.WHILE:
            self.advance()
            stmt = self.while_stmt()
        else:
            stmt = self.generic_stmt()

        return stmt

    def print_stmt(self):
        """\
        <print statement> := "print" <expression> ";"
        """
        stmt = Printer(self.expression())
        self.check_semicolon()
        return stmt

    def block_stmt(self):
        """\
        <block statement> := "{" <declaration>* "}"
        this method returns a list of statements rather than a block node, b/c
        it is used for both generic block statements and function blocks. The
        caller must wrap the list into the appropriate node class.
        """
        stmt_list = []

        while self.curr_type() != TokenType.RIGHT_BRACE:
            expr = self.declaration()
            stmt_list.append(expr)

        if self.curr_type() == TokenType.EOF:
            self.trap("expected '}' at end of file")
        elif self.curr_type() != TokenType.RIGHT_BRACE:
            tok = self.curr_token()
            self.trap("expected '}' at {}".format(tok.lexeme))
        else:
            self.advance()

        return stmt_list

    def branch_stmt(self):
        """\
        <branch> := "if" "(" <expr> ")" <stmt> ("else" <stmt>)?
        """
        if self.curr_type() != TokenType.LEFT_PAREN:
            self.trap("expected open parenthesis after 'if'")
            return Branch(None, None, None)

        self.advance()

        condition = self.expression()

        if self.curr_type() != TokenType.RIGHT_PAREN:
            self.trap("expected close parenthesis after condition")
            return Branch(None, None, None)

        self.advance()

        then_branch = self.statement()
        else_branch = None

        if self.curr_type() == TokenType.ELSE:
            self.advance()
            else_branch = self.statement()

        return Branch(condition, then_branch, else_branch)

    def while_stmt(self):
        """
        <while> := "while" "(" <expression> ")" <statement>
        """
        if self.curr_type() != TokenType.LEFT_PAREN:
            self.trap("expected open parenthesis after 'if'")
            return Loop(None, None)

        self.advance()

        condition = self.expression()

        if self.curr_type() != TokenType.RIGHT_PAREN:
            self.trap("expected close parenthesis after condition")
            return Loop(None, None)

        self.advance()

        body = self.statement()

        return Loop(condition, body)

    def generic_stmt(self):
        """\
        <expression statement> := <expression> ";"
        """
        stmt = Generic(self.expression())
        self.check_semicolon()
        return stmt

    def expression(self):
        """\
        dummy method used to encode the lox grammar explicity in the source.
        <expression> := <assignment>
        """
        return self.assignment()

    def assignment(self):
        """\
        assign rvalue to lvalue
        <assignment> := (IDENTIFIER "=" <assignment>) | <logical or>
        """
        lval = self.logical_or()

        if self.curr_type() == TokenType.EQUAL:
            self.advance()
            rval = self.assignment()

            if isinstance(lval, Variable):
                #extract token from variable node as a valid lvalue
                return Assignment(lval.name, rval)

            self.trap("assignment target is not an l-value")

        #if trap was initiated, this return node is just a dummy.
        #trap synchronized to the next statement anyways so its no risk.
        #on the other hand, if the branch was skipped entirely, then lval
        #is just some expression.
        return lval

    def logical_or(self):
        """\
        <logical or> := <logical and> ("or" <logical and>)*
        """
        expr = self.logical_and()

        if self.curr_type() == TokenType.OR:
            self.advance()

            left = expr
            tok = self.prev_token()
            right = self.logical_and()

            return Logical(left, tok, right)

        return expr

    def logical_and(self):
        """\
        <logical and> := <equality> ("and" <equality>)*
        """
        expr = self.equality()

        if self.curr_type() == TokenType.AND:
            self.advance()

            left = expr
            tok = self.prev_token()
            right = self.logical_and()

            return Logical(left, tok, right)

        return expr

    def equality(self):
        """\
        <equality> := <comparison> (("==" | "!=") <comparison>)*
        """
        expr = self.comparison()

        types = set([TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL])

        while self.curr_type() in types:
            self.advance()

            left = expr
            operator = self.prev_token()
            right = self.comparison()

            expr = Binary(left, operator, right)

        return expr

    def comparison(self):
        """\
        <comparison> := <term> ((">" | "<" | "<=" | ">=") <term>)*
        """
        expr = self.term()

        types = set([TokenType.GREATER, TokenType.GREATER_EQUAL, \
                     TokenType.LESS, TokenType.LESS_EQUAL])

        while self.curr_type() in types:
            self.advance()

            left = expr
            operator = self.prev_token()
            right = self.term()

            expr = Binary(left, operator, right)

        return expr

    def term(self):
        """\
        <term> := <factor> (("+" | "-") <factor>)*
        """
        expr = self.factor()

        while self.curr_type() in set([TokenType.PLUS, TokenType.MINUS]):
            self.advance()

            left = expr
            operator = self.prev_token()
            right = self.factor()

            expr = Binary(left, operator, right)

        return expr

    def factor(self):
        """\
        <factor> := <unary> (("*" | "/") <unary>)*
        """
        expr = self.unary()

        while self.curr_type() in set([TokenType.STAR, TokenType.SLASH]):
            self.advance()

            left = expr
            operator = self.prev_token()
            right = self.unary()

            expr = Binary(left, operator, right)

        return expr

    def unary(self):
        """\
        <unary> := ("!" | "-") <unary> | <primary>
        """
        if self.curr_type() in set([TokenType.BANG, TokenType.MINUS]):
            self.advance()
            return Unary(self.prev_token(), self.unary())

        return self.primary()

    def primary(self):
        """\
        <primary> := NUMBER | STRING | "true" | "false" | "nil"
        <primary> := "(" <expression> ")"
        """
        types = set([TokenType.NUMBER, TokenType.STRING, TokenType.NIL, \
                     TokenType.TRUE, TokenType.FALSE])

        if self.curr_type() in types:
            expr = Literal(self.curr_token())
            self.advance()
        elif self.curr_type() == TokenType.LEFT_PAREN:
            self.advance()
            expr = Grouping(self.expression())

            if self.curr_type() == TokenType.RIGHT_PAREN:
                self.advance()
            else:
                self.trap("missing right parenthesis for grouped expression")
        elif self.curr_type() == TokenType.IDENTIFIER:
            expr = Variable(self.curr_token())
            self.advance()
        elif self.curr_type() == TokenType.EOF:
            #this situation occurs when the user has a grammar error at the
            #end of file such as "3-". In this situation, the parser has been
            #passing the EOF token along the call stack. The else branch can
            #handle this issue, but its not user friendly because it presents
            #a EOF:"None" lexeme to the user.
            #
            #trap is at EOF so no need to create a dummy expr for return
            tok = self.prev_token()
            self.trap("misplaced symbol '{}' at end of file".format(tok.lexeme))
        else:
            lexeme = (self.tokens[self.i]).lexeme
            self.trap("misplaced symbol '{}'".format(lexeme))
            #dummy statement will be added to program tree
            expr = None

        return expr

    def trap(self, msg):
        """\
        push parameters to error handler then enter panic mode to reset at the
        next sequence point.
        """
        tok = self.tokens[self.i]
        line = tok.line

        if not self.err.push(line, msg):
            self.err.grow(1)
            self.error.push(line, "additional errors found (hidden)")

        #synchronize parser to continue at next program statement
        types = set([TokenType.CLASS, TokenType.FUN, TokenType.VAR, \
                     TokenType.FOR, TokenType.IF, TokenType.WHILE, \
                     TokenType.PRINT, TokenType.RETURN])

        while self.curr_type() not in types:
            if self.curr_type() == TokenType.EOF:
                #no statements left in program so no need to continue parsing
                #unwind call stack back to self.program and let it handle return
                raise ParseError
            else:
                self.advance()
