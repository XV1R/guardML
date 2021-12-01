from tokens.TokenType import TokenType
from tokens.token import Token
from main import GuardML

class Scanner:
    def __init__(self, source: str, interpreter: GuardML):
        self.source = source 
        self.tokens = [] #collection of tokens
        self.start = 0 #first character being scanned
        self.current = 0 #current character being looked at
        self.line = 0 #current line 
        self.interpreter = interpreter
        self.digits = ['0','1','2','3','4','5','6','7','8','9']
        self.alpha = [ # lowercase, uppercase, and underscore
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
            'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
            'Y', 'Z',
            '_'
        ]
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'show': TokenType.SHOW,
            'return': TokenType.RETURN,
            'true': TokenType.TRUE,
            'while': TokenType.WHILE,
            'guard': TokenType.GUARD
        }
    def scan_tokens(self):
        while not self.at_end():
            self.scan_token()
            self.start = self.current
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens


    def at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance() 
        match c:
            case '(':
                self.add_token(TokenType.LPAREN)
            case ')':
                self.add_token(TokenType.RPAREN)
            case '{':
                self.add_token(TokenType.LBRACE)
            case '}':
                self.add_token(TokenType.RBRACE)
            case '+':
                self.add_token(TokenType.PLUS)
            case '-':
                if self.check_ahead("-"):
                    while self.peek() != "\n" and not self.at_end:
                        self.advance()
                else:
                    self.add_token(TokenType.MINUS)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '!':
                if self.check_ahead("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case '=':
                if self.check_ahead("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                    self.advance()
                else:
                    self.add_token(TokenType.EQUAL)
            case '<': #TODO
                if self.check_ahead("="): #TODO verify if this works
                    self.add_token(TokenType.LESS_EQUAL)
                    self.advance()
                else:
                    self.add_token(TokenType.LESS)
            case '>':
                if self.check_ahead("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                    self.advance()
                else:
                    self.add_token(TokenType.GREATER)
            case "/":
                self.add_token(TokenType.SLASH)
            case ' ':
                pass    
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line+=1
            case '"':
                self.string()
            case _: #default case; nothing matched
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self.interpreter.error(self.line, err_message="Unexpected character") 
                





    def peek(self):
        if self.at_end(): 
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if (self.current + 1) >= len(self.source):
            return '\0'
        return self.source[self.current + 1]


    def string(self):
        start_line = self.line
        while self.peek() != '"' and not self.at_end:
            if self.peek() == '\n':
                self.line += 1 
            self.advance()

        if self.at_end():
            self.interpreter.error(line=start_line, err_message="Unterminated string.")
            return None 
        
        self.advance() #catch last "
        
        string_content = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, literal=string_content)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        # Look for a decimal
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the '.'
            self.advance()
            # Keep advancing until we reached the end of the number
            while self.is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def is_digit(self, n): 
        return n in self.digits
    
    def is_alpha(self, n):
        return n in self.alpha
            
    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def check_ahead(self, expected = None) -> bool: 
        if self.at_end():
            return False
        if expected is None: 
            return False
        return self.source[self.current+1] == expected
        

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance() 
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENT
        self.add_token(TokenType.IDENT)

    def advance(self) -> str: #moves forward one character
        self.current += 1 
        return self.source[self.current-1]

    def add_token(self, token_type, literal=None) -> None: 
        label = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, label, literal, self.line))