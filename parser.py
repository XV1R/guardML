

from Expr import *
from stmt import *
from tokens.token import Token
from tokens.TokenType import TokenType 


class ParseError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def report(self):
        if self.token.type == TokenType.EOF:
            return f'[line {self.token.line}] Error at end: {self.message}'
        else:
            where = self.token.lexeme
            return f"[line {self.token.line}] Error at '{where}': {self.message}"


class Parser:
    """
    program     = declaration* eof ;

    declaration = varDecl
                | statement ;
    varDecl     = "var" IDENTIFIER ( "=" expression )? ";" ;
    statement   = exprStmt
                | printStmt
                | block ;
    block       = "{" declaration* "}" ;

    exprStmt    = expression ";" ;
    printStmt   = "print" expression ";" ;

    expression  = assignment ;
    assignment  = identifier ( "=" assignment )?
                | equality ;
    equality   → comparison ( ( "!=" | "==" ) comparison )*
    comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*
    term       → factor ( ( "-" | "+" ) factor )*
    factor     → unary ( ( "/" | "*" ) unary )*
    unary      → ( "!" | "-" ) unary
               | primary
    primary    → NUMBER | STRING | "false" | "true" | "nil"
               | "(" expression ")"
               | IDENTIFIER ;
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.LET):
                return self.var_declaration();
            return self.statement();
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        if self.match(TokenType.SHOW): return self.printStatement()
        if self.match(TokenType.LBRACE): return Block(self.block())
        return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def var_declaration(self):
        name = self.consume(TokenType.IDENT, 'Expect variable name.')

        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        else:
            initializer = None

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def block(self):
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, 'Invalid assignment target.')
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if   self.match(TokenType.FALSE):  return Literal(False)
        elif self.match(TokenType.TRUE):   return Literal(True)
        elif self.match(TokenType.NIL):    return Literal(None)
        elif self.match(TokenType.NUMBER,
                        TokenType.STRING): return Literal(self.previous().literal)

        elif self.match(TokenType.IDENT):
            return Variable(self.previous())

        elif self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression")
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect expression')

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()

    def check(self, type: TokenType):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str):
        err = ParseError(token, message)
        self.errors.append(err)
        return err

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in {
                    TokenType.CLASS,
                    TokenType.FUN,
                    TokenType.LET,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.SHOW,
                    TokenType.RETURN,
                }:
                return

            self.advance()
