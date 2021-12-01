from tokens.TokenType import TokenType
from Expr import Expr
# from main import GuardML
from tokens.token import Token


class Parser():
    def __init__(self, tokens: dict()):
        self.tokens = tokens 
        self.current = 0; 

    def parse(self):
        try:
            return self.expression() 
        except self.ParseError:
            return None 

    def expression(self):
        return self.equality() 
        

    class ParseError(RuntimeError):
        pass

    def equality(self):
        expr = self.comparison() 
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous() 
            right = self.comparsion()
            expr = Expr.Binary(expr, operator, right)
        return expr 


    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance() 
                return True
        return False

    def check(self, type):
        if self.at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.at_end():
            self.current += 1 
        return self.previous()

    def at_end(self):
        return self.peek().type == TokenType.EOF;

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def comparison(self) -> Expr:
        expr = self.term() 

        while self.match(TokenType.GREATER_EQUAL, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.LESS):
            operator = self.previous() 
            right = self.term() 
            expr = Expr.Binary(expr, operator, right) 
        return expr 

    def term(self): 
        expr = self.factor() 

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous() 
            right = self.factor() 
            expr = Expr.Binary(expr, operator, right)
        return expr 
    
    def factor(self):
        expr = self.unary() 

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous() 
            right = self.unary() 
            expr = Expr.Binary(expr, operator, right)

        return expr 
    
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous() 
            right = self.unary() 
            return Expr.Unary(operator, right) 
        return self.primary() 

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True) 
        if self.match(TokenType.NIL):
            return Expr.Literal(None) 
        
        if self.match(TokenType.LPAREN):
            expr = self.expression() 
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        self.error(self.peek(), "Expect expression.")
    
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance() 
        self.error(self.peek(), message) 

    def error(self, token: Token, message: str) -> ParseError: 

        # GuardML.error(token, message) 
        print("parser error not specificed")
        return self.ParseError()  

    def synchronize(self) -> None: 
        self.advance() 

        while not self.at_end(): 
            if self.previous().type == TokenType.SEMICOLON:
                return 
            match self.peek().type:
                case TokenType.FUN:
                    pass
                case TokenType.FOR:
                    pass
                case TokenType.IF:
                    pass
                case TokenType.WHILE:
                    pass
                case TokenType.SHOW:
                    pass
                case TokenType.RETURN:
                    return 

            self.advance() 